class SistemaVectores:
    def __init__(self, tamano_entrada, tamano_salida):
        self.vectores_entrada = []
        self.vectores_salida = []

    def agregar_vector(self, vector_entrada, vector_salida):
        self.vectores_entrada.append(vector_entrada)
        self.vectores_salida.append(vector_salida)

    def cargar_datos_desde_archivo(self, archivo):
        with open(archivo, 'r') as file:
            for linea in file:
                partes = linea.strip().split(',')
                entrada = [float(valor) for valor in partes[:-1]]
                salida = float(partes[-1])
                self.agregar_vector(entrada, salida)
