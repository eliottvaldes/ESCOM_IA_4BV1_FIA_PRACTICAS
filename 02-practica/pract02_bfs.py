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
            else:
                color = GRIS
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
    tecla= pygame.key.get_pressed()
    if tecla[pygame.K_w] and fila > 0 and matriz[fila - 1][columna] != 1:
        matriz[fila][columna] = 0
        fila -= 1
    elif tecla[pygame.K_s] and fila < FILA - 1 and matriz[fila + 1][columna] != 1:
        matriz[fila][columna] = 0
        fila += 1
    elif tecla[pygame.K_a] and columna > 0 and matriz[fila][columna - 1] != 1:
        matriz[fila][columna] = 0
        columna -= 1
    elif tecla[pygame.K_d] and columna < COLUMNA - 1 and matriz[fila][columna + 1] != 1:
        matriz[fila][columna] = 0
        columna += 1
    matriz[fila][columna] = PERSONAJE
    posicion_personaje = (fila, columna)

#Oculta la matriz
def ocultaMatriz():
    for fila in range(FILA):
        for columna in range(COLUMNA):
            x = columna * ANCHO_CELDA
            y = fila * ALTO_CELDA
            if matriz[fila][columna] != PERSONAJE:
                pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA))
            else:
                pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CELDA, ALTO_CELDA))  # Deja el personaje visible
                pygame.draw.circle(ventana, AZUL, (x + ANCHO_CELDA // 2, y + ALTO_CELDA // 2), ANCHO_CELDA // 2 - 2)
    pygame.display.flip()

#Restaura el color de las casillas adyacentes al personaje
'''def restaurar_casillas_adyacentes(fila, columna):
    for i in range(max(0, fila - 1), min(FILA, fila + 2)):
        for j in range(max(0, columna - 1), min(COLUMNA, columna + 2)):
            if not (i == fila and j == columna):
                x = j * ANCHO_CELDA
                y = i * ALTO_CELDA
                if matriz[i][j] == 0:
                    color = BLANCO
                else:
                    color = GRIS
                pygame.draw.rect(ventana, color, (x, y, ANCHO_CELDA, ALTO_CELDA))
                pygame.draw.rect(ventana, NEGRO, (x, y, ANCHO_CELDA, ALTO_CELDA), 1)'''

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
        cont = cont - 1
        ocultaMatriz()
        # Restaurar el color original de las casillas adyacentes antes de comenzar a moverse
        '''fila, columna = posicion_personaje
        restaurar_casillas_adyacentes(fila, columna)'''
