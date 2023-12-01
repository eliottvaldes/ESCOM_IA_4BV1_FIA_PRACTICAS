import clasifMinDist
import clasifKNN
import manejoVectores

def main():
    sistema = manejoVectores.SistemaVectores(3, 1)  # Ejemplo con vectores de tamaño 3 y salida 1
    sistema.cargar_datos_desde_archivo('datos.txt')

    clasificador_knn = clasifKNN.clasificador_knn(k=3, tipo_distancia='euclidiana')
    clasificador_knn.agregar_datos_entrenamiento(sistema.vectores_entrada, sistema.vectores_salida)

    clasificador_minima_distancia = clasifMinDist.ClasificadorMinimaDistancia(tipo_distancia='euclidiana')
    clasificador_minima_distancia.agregar_datos_entrenamiento(sistema.vectores_entrada, sistema.vectores_salida)

    # Ejemplo de clasificación con KNN
    resultado_knn = clasificador_knn.clasificar([1, 2, 3])  # Vector de prueba
    print(f"Resultado de clasificación KNN: {resultado_knn}")

    # Ejemplo de clasificación con Mínima Distancia
    resultado_min_dist = clasificador_minima_distancia.clasificar([1, 2, 3])  # Vector de prueba
    print(f"Resultado de clasificación Mínima Distancia: {resultado_min_dist}")

if __name__ == "__main__":
    main()
