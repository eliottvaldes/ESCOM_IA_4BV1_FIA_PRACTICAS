import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores y configuración
NEGRO, BLANCO, GRIS, VERDE, ROJO, AZUL = (0, 0, 0), (255, 255, 255), (128, 128, 128), (0, 255, 0), (255, 0, 0), (0, 0, 255)
ANCHO, ALTO, FILA, COLUMNA, = 600, 600, 15, 15
ANCHO_CELDA, ALTO_CELDA, PERSONAJE= ANCHO // COLUMNA, ALTO // FILA, 4

# Definir matriz y variables de estado
matriz =  [
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

punto_inicial_seleccionado, punto_inicial = False, None
punto_final_seleccionado, punto_final = False, None
posicion_personaje, pasos = None, 0

# Aquí incluirás todas tus funciones definidas (dibujar_matriz, puntoInicial, puntoFinal, etc.)
# Asegúrate de que cada función sea independiente y no utilice variables externas al script.

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

#Cuenta los pasos que se dan
def contarPasos(pasos):
    pasos += 1
    return pasos

class Nodo:
    def __init__(self, fila, columna, padre=None):
        self.fila = fila
        self.columna = columna
        self.padre = padre
        self.hijos = []

def obtener_vecinos(nodo):
    vecinos = []
    # Orden de prioridad modificado: arriba, abajo, izquierda, derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in direcciones:
        nueva_fila, nueva_columna = nodo.fila + dx, nodo.columna + dy
        if 0 <= nueva_fila < FILA and 0 <= nueva_columna < COLUMNA and matriz[nueva_fila][nueva_columna] == 0:
            vecinos.append(Nodo(nueva_fila, nueva_columna, nodo))
    return vecinos

def dfs(inicio, destino):
    fila_inicial, columna_inicial = inicio
    fila_destino, columna_destino = destino
    nodo_inicial = Nodo(fila_inicial, columna_inicial)
    visitado = set()
    pila = [nodo_inicial]

    while pila:
        nodo_actual = pila.pop()
        if (nodo_actual.fila, nodo_actual.columna) == (fila_destino, columna_destino):
            path = []
            while nodo_actual:
                path.append((nodo_actual.fila, nodo_actual.columna))
                nodo_actual = nodo_actual.padre
            return path[::-1], nodo_inicial

        if (nodo_actual.fila, nodo_actual.columna) not in visitado:
            visitado.add((nodo_actual.fila, nodo_actual.columna))

            # Priorizar direcciones: arriba, abajo, izquierda, derecha
            direcciones_priorizadas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in direcciones_priorizadas:
                nueva_fila, nueva_columna = nodo_actual.fila + dx, nodo_actual.columna + dy
                if (0 <= nueva_fila < FILA and 0 <= nueva_columna < COLUMNA and
                    matriz_aux[nueva_fila][nueva_columna] == 0 and
                    (nueva_fila, nueva_columna) not in visitado):
                    nodo_vecino = Nodo(nueva_fila, nueva_columna, nodo_actual)
                    nodo_actual.hijos.append(nodo_vecino)
                    pila.append(nodo_vecino)
    return None, nodo_inicial

def reconstruir_camino(nodo_final):
    camino = []
    nodo_actual = nodo_final
    while nodo_actual is not None:
        camino.append(nodo_actual.valor)
        nodo_actual = nodo_actual.padre
    camino.reverse()
    return camino, nodo_final  # Retornamos la ruta y la raíz del árbol.

def imprimir_arbol_en_formato_de_carpetas(nodo, indent=0):
    if nodo is None:
        return
    espacios = '    ' * indent  # 4 espacios por nivel de indentación
    print(f"{espacios}|- ({nodo.fila}, {nodo.columna})")
    for hijo in nodo.hijos:
        imprimir_arbol_en_formato_de_carpetas(hijo, indent + 1)

ventana = pygame.display.set_mode((ANCHO, ALTO))# Inicializar ventana Pygame
dibujar_matriz()
pygame.display.flip()
# Muestra la matriz y espera a que el usuario seleccione el punto inicial
punto_inicial = puntoInicial()

# Muestra nuevamente la matriz y espera a que el usuario seleccione el punto final
punto_final = puntoFinal()

# Una vez que ambos puntos han sido seleccionados, oculta la matriz
ocultaMatriz()

ruta, nodo_final = dfs(punto_inicial, punto_final)
imprimir_arbol_en_formato_de_carpetas(nodo_final)
if ruta:
    for i in range(1, len(ruta)):
        matriz[ruta[i][0]][ruta[i][1]] = 4  

    print("Ruta encontrada:", ruta)  # para debug

    print("Movimientos realizados:")
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

    print(f"Total de movimientos realizados: {contador_movimientos}")

else:
    print("No se encontró una ruta.")

# Muestra el arbol generado
posicion_personaje = punto_inicial  # inicialización de posicion_personaje
indice_ruta = 1
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ruta and indice_ruta < len(ruta):
        fila, columna = ruta[indice_ruta]
        matriz[posicion_personaje[0]][posicion_personaje[1]] = 0
        matriz[fila][columna] = PERSONAJE
        posicion_personaje = (fila, columna)
        indice_ruta += 1
        pygame.time.delay(200)  # Agregar un retraso para ver el movimiento

    dibujar_matriz()
    pygame.display.flip()