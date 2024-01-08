"""
Respira profundo, lee lentamente y piensa paso a paso.
Usando python debes hacer lo siguiente:
1.- crear una interfaz grafica en la que se muestre un laberinto dado una matriz de 1 y 0.
2.- el sistema debe permitirle al usuario seleccionar uno de los 4 personajes (humano, mono, pulpo, pie grande)
3.- el usuario puede seleccionar el punto de partida de su personaje dentro del laberinto.
3.1 El sistema debe validar que el punto de partida seleccionado no sea un punto no permitido por el personaje.
4.- el usuario puede seleccionar el punto de llegada de su personaje dentro del laberinto.
4.1 El sistema debe validar que el punto de llegada seleccionado no sea un punto no permitido por el personaje.
4.2.- el sistema debe de colocar un puntito rojo en el punto de partida y un puntito verde en el punto de llegada.
5.- el sistema debe de encontrar la ruta más indicada usando el argoritmo A estrella. La funcion debe devolver los nodos abiertos, los nodos cerrados, el arbol generado y la ruta ideal.
6.- El sistema debe mover el personaje por el laberinto segun la ruta ideal del algoritmo A estrella.
7.- El sistema debe de colocar en el laberinto la notación en texto indicada en los pasos siguientes:
7.1- El sistema debe colocar una letra 'O' en laberinto segun sean los nodos abiertos del algoritmo a estrella.
7.2.- El sistema debe colocar una letra 'X' en laberinto segun sean los nodos cerrados del algoritmo a estrella.
7.3- El sistema debe colocar entre parentesis el costo total del movimiento en cada una de las celdas visitadas por el algoritmo A estrella. Ejemplo de un nodo abierto con costo de 5: O(5). Ejemplo de un nodo cerrado con costo de 2: X(2).
8.- El sistema debe de imprimir en terminal el arbol generado con la solución del algoritmo a estrella. El formato de impresión del arbol debe ser como un directorio de carpetas, es decir, por niveles y saltos de linea.

NOTAS:
+ el sistema debe de tomar en cuenta los pesos del laberinto ya que cambian de  a cuerdo al personaje seleccionado
+ el sistema debe de considerar que la matriz está creada usando los colores definidos en colorDictionary
+ el sistema debe detectar si un personaje no puede pasar por una celda que se identifica en cada personaje con el valor de 'fieldsNotAllowed'

---
Toma en cuenta el codigo ya existente:

"""

import pygame
import sys
from queue import PriorityQueue
import time

# Constantes
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
CELL_SIZE = 40  # Asumiendo que cada celda del laberinto es un cuadrado de 40x40

# Colores
colorDictionary = {
    "0": (128, 128, 128),  # Gris
    "1": (255, 203, 164),  # Tierra
    "2": (10, 191, 178),   # Agua
    "3": (255, 175, 7),    # Arena
    "4": (17, 243, 64),    # Bosque
    "5": (128, 0, 128),    # Pantano
    "6": (255, 255, 255),  # Nieve
}

# Matriz del laberinto
mazeMatrix = [["4","4","4","1","1","1","1","1","1","1","1","1","1","4","4"],["4","4","4","4","4","4","1","1","1","1","4","3","4","4","4"],["4","4","4","2","2","4","1","4","1","1","3","3","4","1","1"],["4","4","2","2","2","2","1","4","1","1","3","3","1","1","1"],["4","4","2","2","2","2","1","4","4","1","1","3","1","1","1"],["4","4","4","2","2","1","1","1","1","1","1","3","3","3","3"],["4","4","4","0","0","0","1","1","1","1","1","3","3","3","3"],["4","4","4","1","0","4","4","1","1","3","3","3","3","2","2"],["4","4","4","1","1","4","4","0","1","3","3","3","2","2","2"],["4","4","1","1","1","1","0","0","0","3","3","2","2","2","2"],["4","4","1","1","1","1","1","1","3","3","3","2","2","2","2"],["4","4","1","1","1","1","1","1","3","3","2","2","2","2","2"],["4","4","1","4","4","1","1","3","3","3","2","2","2","2","2"],["4","4","4","4","4","4","1","3","3","3","2","2","2","2","2"],["4","4","4","4","4","4","1","3","3","3","2","2","2","2","2"]]

characters = {
    'person': {
        'id': 1,
        'name': 'Humano',
        'icon': '👨',
        'fieldsNotAllowed': ['0'],  # negro - montaña
        'heights': {
            # color_index: peso_de_movi
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
        }
    },
    'monkey': {
        'id': 2,
        'name': 'Mono',
        'icon': '🐒',
        'fieldsNotAllowed': ['0', '6'],  # negro - montaña
        'heights': {
            # color_index: peso_de_movi
            0: 0,
            1: 2,
            2: 4,
            3: 3,
            4: 1,
            5: 5,
            6: 0,
        }
    },
    'octopus': {
        'id': 3,
        'name': 'Pulpo',
        'icon': '🐙',
        'fieldsNotAllowed': ['0', '3', '6'],
        'heights': {
            # color_index: peso_de_movi
            0: 0,
            1: 2,
            2: 1,
            3: 0,
            4: 3,
            5: 2,
            6: 0,
        }
    },
    'sasquatch': {
        'id': 4,
        'name': 'Pie grande',
        'icon': '🦶',
        'fieldsNotAllowed': ['2', '3'],
        'heights': {
            # color_index: peso_de_movi
            0: 15,
            1: 4,
            2: 0,
            3: 0,
            4: 4,
            5: 5,
            6: 3,
        }
    }    
}

# Inicialización de Pygame
pygame.init()
# Define una fuente para el texto
font_size = 20
font = pygame.font.Font(None, font_size)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Laberinto A*")


def main():
    running = True
    
    character = select_character()  # Selección del personaje     
    start_point = select_point("Seleccione el punto de partida", character, validate_point)
    end_point = select_point("Seleccione el punto de llegada", character, validate_point)
    draw_start_end_points(start_point, end_point)  # Dibujar puntos de inicio y fin
    # Llamada a a_star_search    
    try:
        path, g_score, f_score, came_from = a_star_search(start_point, end_point, character)
        print("Ruta encontrada:", path)
        move_character(path, character)  # Aquí mueves el personaje a través de la ruta.
    except ValueError as e:
        print("Error en la búsqueda de ruta:", e)
        return

    # Procesamiento de los resultados
    open_nodes = set(f_score) - set(g_score)  # Nodos que estaban en open_set pero no en closed_set
    closed_nodes = set(g_score)  # Nodos que fueron completamente explorados


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze()
        
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

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_score, f_score, came_from

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
        pygame.time.wait(1000)  # Espera 1 segundo entre cada movimiento
        clear_character(position)
    else:
        print("Personaje ha llegado a su destino.")

def draw_character(position, character):
    x, y = position
    center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
    
    pygame.draw.circle(screen, (0, 0, 0), center, CELL_SIZE // 2)    
    

def clear_character(position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colorDictionary[mazeMatrix[y][x]], rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Redibuja el borde de la celda.



if __name__ == "__main__":
    main()