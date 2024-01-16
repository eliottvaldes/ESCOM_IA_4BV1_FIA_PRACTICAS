import pygame
import sys
from collections import deque

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tamaños y configuración
ANCHO = 600
ALTO = 600
FILA = 15
COLUMNA = 15
ANCHO_CELDA = ANCHO // COLUMNA
ALTO_CELDA = ALTO // FILA
PERSONAJE = 4

# Definir la nueva matriz
matriz = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1 ,0 ,1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
]

#Defines an auxiliar matrix with the same value as the original
matriz_aux = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1 ,0 ,1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
]
# Inicializar Pygame ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Practica 2")

# Variables para el punto inicial
punto_inicial_seleccionado = False
punto_inicial = None

# Variables para el punto final
punto_final_seleccionado = False
punto_final = None

#variables para generar personaje
PERSONAJE = 4
posicion_personaje = None
pasos=0

def dibujar_matriz():
    for fila in range(FILA):
        for columna in range(COLUMNA):
            # Calcular las coordenadas de la celda
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA
            # Dibujar el fondo de la celda
            if matriz[fila][columna] == 0:
                color = BLANCO
            if matriz[fila][columna] ==1:
                color = GRIS
            if matriz[fila][columna] == 2:
                color = NEGRO
            pygame.draw.rect(ventana, color, (x, y, ANCHO_CELDA, ALTO_CELDA))
            # Dibujar el contorno de la celda
            pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA), 1)
            # Dibujar la selección verde si el punto inicial está seleccionado
            if punto_inicial_seleccionado and punto_inicial == (fila, columna):
                pygame.draw.rect(ventana, VERDE, (x, y, ANCHO_CELDA, ALTO_CELDA), 4)
            # Dibujar la selección roja si el punto final está seleccionado
            if punto_final_seleccionado and punto_final == (fila, columna):
                pygame.draw.rect(ventana, ROJO, (x, y, ANCHO_CELDA, ALTO_CELDA), 4)
            # Dibujar al personaje en la posición inicial
            if posicion_personaje and posicion_personaje == (fila, columna):
                pygame.draw.circle(ventana, AZUL, (x + ANCHO_CELDA // 2, y + ALTO_CELDA // 2), ANCHO_CELDA // 2 - 2)

# Función para definir el punto inicial mediante clic de mouse
def puntoInicial():
    global punto_inicial_seleccionado, punto_inicial, posicion_personaje
    punto_inicial_seleccionado = True
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and punto_inicial_seleccionado:
                x, y = pygame.mouse.get_pos()
                if matriz[y // ALTO_CELDA][x // ANCHO_CELDA] != 1:
                    fila = y // ALTO_CELDA
                    columna = x // ANCHO_CELDA
                    punto_inicial = (fila, columna)
                    matriz[fila][columna] = PERSONAJE  # Marcar la posición del personaje
                    posicion_personaje = punto_inicial
                    print(f"Punto Inicial: {punto_inicial}")
                    return punto_inicial

# Función para definir el punto final mediante clic de mouse
def puntoFinal():
    global punto_final_seleccionado, punto_final
    punto_final_seleccionado = True
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and punto_final_seleccionado:
                x, y = pygame.mouse.get_pos()
                #verifica que la posicion marcada no sea un 1 dentro de la matriz
                if matriz[y // ALTO_CELDA][x // ANCHO_CELDA] != 1:
                    fila = y // ALTO_CELDA
                    columna = x // ANCHO_CELDA
                    punto_final = (fila, columna)
                    print(f"Punto Final: {punto_final}")
                    return punto_final


def ocultaMatriz():
    for fila in range(FILA):
        for columna in range(COLUMNA):
            if (fila, columna) != posicion_personaje:
                matriz[fila][columna] = 2

def descubrir_casillas_adyacentes(fila, columna):
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        nueva_fila, nueva_columna = fila + dx, columna + dy
        if 0 <= nueva_fila < FILA and 0 <= nueva_columna < COLUMNA:
            matriz[nueva_fila][nueva_columna] = matriz_aux[nueva_fila][nueva_columna]

def restaurar_casillas_adyacentes(fila, columna):
    for i in range(max(0, fila - 1), min(FILA, fila + 2)):
        for j in range(max(0, columna - 1), min(COLUMNA, columna + 2)):
            matriz[i][j] = matriz_aux[i][j]

#Cuenta los pasos que se dan
def contarPasos(pasos):
    pasos += 1
    return pasos

# Clase nodo para el algoritmo BFS
class Nodo:
    def __init__(self, fila, columna, padre=None):
        self.fila = fila
        self.columna = columna
        self.padre = padre
        self.hijos = []

# Función BFS para encontrar la ruta más corta
def bfs(inicio, destino):
    fila_inicial, columna_inicial = inicio
    fila_destino, columna_destino = destino
    nodo_inicial = Nodo(fila_inicial, columna_inicial)
    visitado = set()
    cola = deque([nodo_inicial])

    while cola:
        nodo_actual = cola.popleft()
        if (nodo_actual.fila, nodo_actual.columna) == (fila_destino, columna_destino):
            path = []
            while nodo_actual:
                path.append((nodo_actual.fila, nodo_actual.columna))
                nodo_actual = nodo_actual.padre
            return path[::-1], nodo_inicial

        # Priorizar direcciones: arriba, abajo, izquierda, derecha
        direcciones_priorizadas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in direcciones_priorizadas:
            nueva_fila, nueva_columna = nodo_actual.fila + dx, nodo_actual.columna + dy
            if (0 <= nueva_fila < FILA and 0 <= nueva_columna < COLUMNA and
                matriz_aux[nueva_fila][nueva_columna] == 0 and
                (nueva_fila, nueva_columna) not in visitado):
                visitado.add((nueva_fila, nueva_columna))
                nodo_vecino = Nodo(nueva_fila, nueva_columna, nodo_actual)
                nodo_actual.hijos.append(nodo_vecino)
                cola.append(nodo_vecino)
    return None, nodo_inicial


def imprimir_arbol_bfs_por_niveles(raiz):
    if raiz is None:
        return

    cola = deque([(raiz, 0, "")])  # Cola con tuplas de (nodo, nivel, prefijo)

    while cola:
        nodo_actual, nivel, prefijo = cola.popleft()

        # Preparar la conexión del árbol para este nodo
        conexion = "└── " if prefijo.endswith("    ") or prefijo == "" else "├── "

        # Imprimir el nodo actual con el prefijo adecuado
        print(f"{prefijo}{conexion}({nodo_actual.fila}, {nodo_actual.columna})")

        # Preparar el nuevo prefijo para los hijos de este nodo
        nuevo_prefijo = prefijo + ("    " if conexion == "└── " else "|   ")

        for i, hijo in enumerate(nodo_actual.hijos):
            # Si es el último hijo, la conexión debe ser diferente
            if i == len(nodo_actual.hijos) - 1:
                cola.append((hijo, nivel + 1, nuevo_prefijo))
            else:
                cola.append((hijo, nivel + 1, nuevo_prefijo + "|   "))

dibujar_matriz()
pygame.display.flip()

# Muestra la matriz y espera a que el usuario seleccione el punto inicial
punto_inicial = puntoInicial()

# Muestra nuevamente la matriz y espera a que el usuario seleccione el punto final
punto_final = puntoFinal()

# Una vez que ambos puntos han sido seleccionados, oculta la matriz
ocultaMatriz()



ruta, raiz = bfs(punto_inicial, punto_final)
imprimir_arbol_bfs_por_niveles(raiz)

if ruta is None:
    print("No hay una ruta válida entre el punto inicial y el punto final.")
    sys.exit()

print("\nMovimientos realizados:")
contador_movimientos = 0
for i in range(1, len(ruta)):
    fila_actual, columna_actual = ruta[i]
    fila_anterior, columna_anterior = ruta[i-1]
    
    if fila_actual == fila_anterior - 1:
        print("Arriba")
        contador_movimientos += 1
    elif fila_actual == fila_anterior + 1:
        print("Abajo")
        contador_movimientos += 1
    elif columna_actual == columna_anterior - 1:
        print("Izquierda")
        contador_movimientos += 1
    elif columna_actual == columna_anterior + 1:
        print("Derecha")
        contador_movimientos += 1

# Imprime el total de movimientos
print(f"\nTotal de movimientos realizados: {contador_movimientos}")

indice_ruta = 1  
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if indice_ruta < len(ruta):
        fila, columna = ruta[indice_ruta]
        descubrir_casillas_adyacentes(fila, columna)
        matriz[posicion_personaje[0]][posicion_personaje[1]] = 0
        matriz[fila][columna] = PERSONAJE
        posicion_personaje = (fila, columna)
        indice_ruta += 1
        pygame.time.delay(200)  # Agregar un retraso para ver el movimiento

    # Dibujar la matriz en la ventana
    dibujar_matriz()
    # Actualizar la pantalla
    pygame.display.flip()
