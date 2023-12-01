import numpy as np
import clasifKNN

class ClasificadorMinimaDistancia:
    def __init__(self, tipo_distancia='euclidiana'):
        self.tipo_distancia = tipo_distancia
        self.vectores_entrenamiento = []
        self.etiquetas_entrenamiento = []

    def agregar_datos_entrenamiento(self, vectores_entrenamiento, etiquetas_entrenamiento):
        self.vectores_entrenamiento = vectores_entrenamiento
        self.etiquetas_entrenamiento = etiquetas_entrenamiento

    # Reutilizamos la función calcular_distancia de ClasificadorKNN

    def clasificar(self, vector):
        distancias = [clasifKNN.calcular_distancia(self, vector, vector_entrenamiento)
                for vector_entrenamiento in self.vectores_entrenamiento]
        indice_minimo = np.argmin(distancias)
        return self.etiquetas_entrenamiento[indice_minimo]
