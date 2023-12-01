import numpy as np

class ClasificadorKNN:
    def __init__(self, k, tipo_distancia='euclidiana'):
        self.k = k
        self.tipo_distancia = tipo_distancia
        self.vectores_entrenamiento = []
        self.etiquetas_entrenamiento = []

    def agregar_datos_entrenamiento(self, vectores_entrenamiento, etiquetas_entrenamiento):
        self.vectores_entrenamiento = vectores_entrenamiento
        self.etiquetas_entrenamiento = etiquetas_entrenamiento

    def calcular_distancia(self, vector1, vector2):
        if self.tipo_distancia == 'euclidiana':
            return np.linalg.norm(np.array(vector1) - np.array(vector2))
        elif self.tipo_distancia == 'manhattan':
            return np.sum(np.abs(np.array(vector1) - np.array(vector2)))
        else:
            raise ValueError("Tipo de distancia no soportado")

    def clasificar(self, vector):
        distancias = [self.calcular_distancia(vector, vector_entrenamiento)
                    for vector_entrenamiento in self.vectores_entrenamiento]
        indices_ordenados = np.argsort(distancias)
        votos = np.array(self.etiquetas_entrenamiento)[indices_ordenados][:self.k]
        (valores, cuenta) = np.unique(votos, return_counts=True)
        indice_mayoria = np.argmax(cuenta)
        return valores[indice_mayoria]
