import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Plab: Carga de datos
# Adair, Ethel, Leobardo, Eliot

class DataLoader:
    def __init__(self):
        self.data = None

    def load_data(self, delimiter=','):
        try:
            # Crear una ventana para seleccionar el archivo
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Seleccionar archivo de datos", filetypes=[("Archivos CSV", "*.csv")])

            # Verificar si el usuario ha seleccionado un archivo
            if not file_path:
                print("No se ha seleccionado ningún archivo.")
                return

            # Cargar el archivo de texto plano
            self.data = pd.read_csv(file_path, delimiter=delimiter)

            # Imprimir el número de atributos y patrones
            num_attributes = len(self.data.columns)
            num_patterns = len(self.data)

            print(f"Número de atributos: {num_attributes}")
            print(f"Número de patrones: {num_patterns}")

            return file_path

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def select_attributes(self, attribute_indices):
        try:
            # Seleccionar un subconjunto de atributos
            selected_data = self.data.iloc[:, attribute_indices]

            # Imprimir la información del subconjunto
            print("\nSubconjunto de atributos seleccionados:")
            print(selected_data)

            #  el programa mostrará el subconjunto de atributos seleccionados en la salida.
            #  Guarda ese subconjunto en un archivo txt plano llamado subset_attributes.txt
            selected_data.to_csv("subset_attributes.txt", index=False)

        except Exception as e:
            print(f"Error al seleccionar atributos: {e}")

    def select_rows(self, row_indices):
        try:
            # Seleccionar un subconjunto de renglones
            selected_data = self.data.iloc[row_indices, :]

            # Imprimir la información del subconjunto
            print("\nSubconjunto de renglones seleccionados:")
            print(selected_data)

            # Guardar el subconjunto en un archivo txt plano
            selected_data.to_csv("subset_rows.txt", index=False)

        except Exception as e:
            print(f"Error al seleccionar renglones: {e}")

if __name__ == "__main__":
    # Crear una instancia del DataLoader
    data_loader = DataLoader()

    # Cargar los datos y obtener la ruta del archivo
    file_path = data_loader.load_data()

    if file_path:
        # Seleccionar un subconjunto de atributos
        #Los índices de atributos corresponden a las columnas en el conjunto de datos cargado.
        attribute_indices = list(map(int, input("Ingrese los índices de los atributos separados por espacio: ").split()))
        data_loader.select_attributes(attribute_indices)

        # Seleccionar un subconjunto de renglones
        row_indices = list(map(int, input("Ingrese los índices de los renglones separados por espacio: ").split()))
        data_loader.select_rows(row_indices)

