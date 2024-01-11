import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Función para calcular la distancia euclidiana entre dos filas
def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return distance ** 0.5

# Función para clasificar un punto de prueba usando el algoritmo KNN
def knn_classify(data, test_row, num_neighbors):
    distances = []
    for idx, row in data.iterrows():
        dist = euclidean_distance(test_row, row)
        distances.append((row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = distances[:num_neighbors]
    
    output_values = [row[-1] for row, _ in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction

# Función para el clasificador de distancia mínima
def minimum_distance_classifier(train_data, test_row):
    class_means = train_data.groupby(train_data.columns[-1]).mean()
    min_distance = float('inf')
    prediction = None
    for class_value, class_mean in class_means.iterrows():
        dist = euclidean_distance(class_mean, test_row)
        if dist < min_distance:
            min_distance = dist
            prediction = class_value
    return prediction

# Clase para manejar la carga y clasificación de datos
class DataLoader:
    def __init__(self):
        self.data = None

    # Clasifica los datos utilizando KNN y el clasificador de distancia mínima
    def classify_data(self, k):
        for index, row in self.data.iterrows():
            knn_prediction = knn_classify(self.data, row, k)
            min_dist_prediction = minimum_distance_classifier(self.data, row)
            print(f"Row {index} - Real: {row[-1]}, KNN: {knn_prediction}, MinDist: {min_dist_prediction}")

    # Carga datos desde un archivo CSV seleccionado por el usuario
    def load_data(self, delimiter=','):
        try:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Seleccionar archivo de datos", filetypes=[("Archivos CSV", "*.csv")])

            if not file_path:
                print("No se ha seleccionado ningún archivo.")
                return

            self.data = pd.read_csv(file_path, delimiter=delimiter)
            num_attributes = len(self.data.columns)
            num_patterns = len(self.data)
            print(f"Número de atributos: {num_attributes}")
            print(f"Número de patrones: {num_patterns}")

            return file_path

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    # Selecciona un subconjunto de atributos del conjunto de datos
    def select_attributes(self, attribute_indices):
        try:
            selected_data = self.data.iloc[:, attribute_indices]
            print("\nSubconjunto de atributos seleccionados:")
            print(selected_data)
            selected_data.to_csv("subset_attributes.txt", index=False)

        except Exception as e:
            print(f"Error al seleccionar atributos: {e}")

    # Selecciona un subconjunto de filas del conjunto de datos
    def select_rows(self, row_indices):
        try:
            selected_data = self.data.iloc[row_indices, :]
            print("\nSubconjunto de renglones seleccionados:")
            print(selected_data)
            selected_data.to_csv("subset_rows.txt", index=False)

        except Exception as e:
            print(f"Error al seleccionar renglones: {e}")


if __name__ == "__main__":
    data_loader = DataLoader()
    file_path = data_loader.load_data()

    if file_path:
        attribute_indices = list(map(int, input("Ingrese los índices de los atributos separados por espacio: ").split()))
        data_loader.select_attributes(attribute_indices)

        row_indices = list(map(int, input("Ingrese los índices de los renglones separados por espacio: ").split()))
        data_loader.select_rows(row_indices)

    k = int(input("\nIngrese el número de vecinos para KNN: "))
    data_loader.classify_data(k)
