import pygame
import sys
from queue import PriorityQueue
import time
from global_variables import colorDictionary, mazeMatrix, characters

# Constantes
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
CELL_SIZE = 40  # Asumiendo que cada celda del laberinto es un cuadrado de 40x40


# Inicialización de Pygame
pygame.init()
# Define una fuente para el texto
font_size = 20
font = pygame.font.Font(None, font_size)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laberinto A*")


# Variables globales para los puntos de inicio y fin
global start_point, end_point

def main():
    global start_point, end_point
    running = True
    
    character = select_character()  # Selección del personaje     
    start_point = select_point("Seleccione el punto de partida", character, validate_point)
    end_point = select_point("Seleccione el punto de llegada", character, validate_point)
    change_maze_color_black()


    # Llamada a a_star_search    
    try:        
        path, g_score, f_score, came_from, open_nodes, closed_nodes = a_star_search(start_point, end_point, character)       
        print_tree(came_from, start_point)        
        print("Ruta encontrada:", path)       
        # Actualiza el laberinto para mostrar nodos abiertos/cerrados en color
        update_maze_with_open_closed_nodes(open_nodes, closed_nodes) 
        move_character(path, character)
    except ValueError as e:
        print("Error en la búsqueda de ruta:", e)
        return    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze()
        draw_start_end_points(start_point, end_point)  # Asegúrate de dibujar los puntos de inicio y fin
        draw_open_closed_nodes(open_nodes, closed_nodes)  # Dibuja nodos abiertos y cerrados
        draw_optimal_route(path)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# funcion para dibujar el laberinto
def draw_maze():
    for y, row in enumerate(mazeMatrix):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, colorDictionary[cell], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

# funcion para crear los botones de seleccion de personaje
def create_character_buttons():
    button_width, button_height = 100, 50
    buttons = {}
    x = 20  # Posición inicial x para el primer botón
    y = 20  # Posición inicial y para los botones

    for character_key, character_info in characters.items():
        buttons[character_key] = pygame.Rect(x, y, button_width, button_height)
        x += button_width + 25  # Ajusta el espacio entre los botones

    return buttons

# funcion para seleccionar el personaje usando los botones
def select_character():
    character_button_rect = create_character_buttons()
    selected_character = None
    while selected_character is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for character_key, rect in character_button_rect.items():
                    if rect.collidepoint(mouse_pos):
                        selected_character = character_key
                        break

        screen.fill((200, 225, 255))  # Fondo para la selección de personajes

        # Dibuja los botones y el nombre de los personajes
        for character_key, rect in character_button_rect.items():
            pygame.draw.rect(screen, (0, 0, 255), rect)  # Dibuja rectángulos como botones

            # Renderiza el nombre del personaje en el botón
            text_surface = font.render(characters[character_key]['name'], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

    return selected_character


def select_point(message, character, validation_function):    
    print(message)
    point = None
    while point is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                cell_x, cell_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                if 0 <= cell_x < len(mazeMatrix[0]) and 0 <= cell_y < len(mazeMatrix):
                    point = (cell_x, cell_y)
                    if not validation_function(character, point):
                        print("Punto no válido, seleccione otro.")
                        point = None  # Reiniciar la selección de punto
                    else:
                        print(f"Punto seleccionado: {point}")

        screen.fill((0, 0, 0))  # Fondo negro
        draw_maze()
        pygame.display.flip()

    return point


# funcion para validar que los puntos seleccionados son validos
def validate_point(character, selected_point):    
    cell_value = mazeMatrix[selected_point[1]][selected_point[0]]
    if cell_value in characters[character]['fieldsNotAllowed']:
        return False
    return True 
    

# funcion para dibujar los puntos de partida y puntos de llegada
def draw_start_end_points(start_point, end_point):    
    start_center = (start_point[0] * CELL_SIZE + CELL_SIZE // 2, start_point[1] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (0, 0, 0), start_center, CELL_SIZE // 2)  # Círculo negro para el inicio

    end_center = (end_point[0] * CELL_SIZE + CELL_SIZE // 2, end_point[1] * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (0, 0, 255), end_center, CELL_SIZE // 2)  # Círculo azul para el fin


"""
ALGORITMO A ESTRELLA
"""
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(start, goal, character):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set_hash = {start}
    closed_set = set()  # Conjunto de nodos cerrados
    # Variables para almacenar nodos abiertos y cerrados
    open_nodes = set()
    closed_nodes = set()

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)
        closed_set.add(current)  # Añade el nodo actual al conjunto de cerrados
        
        open_nodes.update(open_set_hash)  # Almacena nodos abiertos
        closed_nodes.update(closed_set)   # Almacena nodos cerrados
        
        if current == goal:            
            return reconstruct_path(came_from, current), g_score, f_score, came_from, open_nodes, closed_nodes


        for neighbor in neighbors(current, character):
            tentative_g_score = g_score[current] + get_cost(current, neighbor, character)

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    raise ValueError("No Path Found")

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]  # Return reversed path

def neighbors(node, character):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
    result = []
    for dir in directions:
        next_node = (node[0] + dir[0], node[1] + dir[1])
        if 0 <= next_node[0] < len(mazeMatrix[0]) and 0 <= next_node[1] < len(mazeMatrix):
            if mazeMatrix[next_node[1]][next_node[0]] not in characters[character]['fieldsNotAllowed']:
                result.append(next_node)
    return result

def get_cost(a, b, character):
    ax, ay = a
    bx, by = b
    cell_value = mazeMatrix[by][bx]
    cell_index = int(cell_value)
    return characters[character]['heights'][cell_index]

"""
MOVIMIENTO DE PERSONAJES
"""

def move_character(path, character):
    for position in path:
        draw_character(position, character)
        pygame.display.flip()
        pygame.time.wait(500)  # Espera 1 segundo entre cada movimiento
        clear_character(position)    
                

def draw_character(position, character):
    x, y = position
    center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
    
    pygame.draw.circle(screen, (0, 0, 0), center, CELL_SIZE // 2)    
    

def clear_character(position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colorDictionary[mazeMatrix[y][x]], rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Redibuja el borde de la celda.


"""
ARBOL GENERADO
"""
def print_tree(tree, start, level=0):
    indent = ' ' * (level * 4)  # 4 espacios por nivel de indentación
    print(f"{indent}- {start}")
    children = [node for node, parent in tree.items() if parent == start]
    for child in children:
        print_tree(tree, child, level + 1)



"""
MOSTRAR NODOS ABIERTOS Y CERRADOS
"""
def draw_open_closed_nodes(open_set_hash, closed_set):
    for node in closed_set:
        x, y = node
        text_surface = font.render('X', True, (0, 0, 255))  # Verde para nodos cerrados
        screen.blit(text_surface, (x * CELL_SIZE, y * CELL_SIZE))
        
    for node in open_set_hash:
        if node not in closed_set:
            x, y = node
            text_surface = font.render('O', True, (255, 0, 0))  # Rojo para nodos abiertos
            screen.blit(text_surface, (x * CELL_SIZE, y * CELL_SIZE))

    
# Función para dibujar la ruta óptima en el laberinto
def draw_optimal_route(path):
    for position in path:
        x, y = position
        text_surface = font.render('R', True, (255, 255, 255))  # Verde para la ruta óptima
        screen.blit(text_surface, ( (x * CELL_SIZE) + 15, (y * CELL_SIZE) + 15) )

# Función para cambiar todo el laberinto a negro con bordes blancos
def change_maze_color_black():
    for y in range(len(mazeMatrix)):
        for x in range(len(mazeMatrix[0])):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

# Función para actualizar el laberinto con los nodos abiertos y cerrados en color
def update_maze_with_open_closed_nodes(open_nodes, closed_nodes):
    for y, row in enumerate(mazeMatrix):
        for x, cell in enumerate(row):
            if (x, y) in open_nodes or (x, y) in closed_nodes:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, colorDictionary[cell], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)



"""
RUN MAIN FUNCION
"""
if __name__ == "__main__":
    main()