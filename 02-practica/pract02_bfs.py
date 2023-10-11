import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO= (255, 0, 0)
AZUL=(0,0,255)
# Tamaño de la ventana y de la matriz
ANCHO = 600
ALTO = 600
FILA = 15
COLUMNA = 15

# Tamaño de cada celda
ANCHO_CELDA = ANCHO // COLUMNA
ALTO_CELDA = ALTO // FILA

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
# Inicializar Pygame
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

# Función para manejar el movimiento del personaje
def mover_personaje(tecla):
    global posicion_personaje

    fila, columna = posicion_personaje
    tecla = pygame.key.get_pressed()

    # Guardar las posiciones adyacentes antes de mover al personaje
    restaurar_casillas_adyacentes(fila, columna)

    nueva_fila, nueva_columna = fila, columna

    if tecla[pygame.K_w] and fila > 0 and matriz_aux[fila - 1][columna] == 0:
        nueva_fila -= 1
    elif tecla[pygame.K_s] and fila < FILA - 1 and matriz_aux[fila + 1][columna] == 0:
        nueva_fila += 1
    elif tecla[pygame.K_a] and columna > 0 and matriz_aux[fila][columna - 1] == 0:
        nueva_columna -= 1
    elif tecla[pygame.K_d] and columna < COLUMNA - 1 and matriz_aux[fila][columna + 1] == 0:
        nueva_columna += 1

    # Verificar si la nueva posición es válida en la matriz original
    if 0 <= nueva_fila < FILA and 0 <= nueva_columna < COLUMNA and matriz[nueva_fila][nueva_columna] == 0:
        # Actualizar la matriz original y la auxiliar
        matriz[fila][columna] = matriz_aux[fila][columna]
        matriz_aux[fila][columna] = 0

        fila, columna = nueva_fila, nueva_columna
        matriz_aux[fila][columna] = PERSONAJE
        posicion_personaje = (fila, columna)

        # Restaurar las casillas adyacentes en la matriz original después del movimiento
        restaurar_casillas_adyacentes(fila, columna)

#Function that hides the matrix except the character
def ocultaMatriz():
    for fila in range(FILA):
        for columna in range(COLUMNA):
            if matriz[fila][columna] != PERSONAJE:
                matriz[fila][columna] = 2

# Function that shows the matrix as the character explores, replacing the values on the modified matrix with the auxiliar matrix
def restaurar_matriz():
    for fila in range(FILA):
        for columna in range(COLUMNA):
            matriz[fila][columna] = matriz_aux[fila][columna]

def restaurar_casillas_adyacentes(fila, columna):
    for i in range(max(0, fila - 1), min(FILA, fila + 2)):
        for j in range(max(0, columna - 1), min(COLUMNA, columna + 2)):
            matriz[i][j] = matriz_aux[i][j]

# Bucle principal
cont = 1
destino = 0
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if punto_inicial_seleccionado and destino == 0:
                mover_personaje(evento.key)
                # Verificar si se llegó al destino
                if posicion_personaje == punto_final:
                    print("Llegaste a tu destino!")
                    destino = 1
    # Dibujar la matriz en la ventana
    dibujar_matriz()
    # Actualizar la pantalla
    pygame.display.flip()

    if cont:
        puntoInicial()
        puntoFinal()
        ocultaMatriz()
        cont = cont - 1