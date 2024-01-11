# Importación de bibliotecas necesarias
from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np

# Definición de un diccionario con identificadores de conjuntos de datos
datasets = {
    "Eliot": 53,  # Iris
    "Ethel": 17,  # Cancer
    "Leo": 878,   # Cirrhosis
    "Adair": 19, # Wine
}

# Carga de un conjunto de datos específico desde el repositorio UCI
dataset = fetch_ucirepo(id=datasets["Eliot"])

# Extracción de características y etiquetas del conjunto de datos
X = dataset.data.features  # Características
y = dataset.data.targets   # Etiquetas
df = pd.DataFrame(X, columns=dataset.data.feature_names)
df['target'] = y           # Añadir etiquetas como una columna adicional

# Eliminación de filas con valores faltantes
df = df.dropna()

# Función para separar el dataframe en características (X) y etiquetas (y)
def separate_dataframe(df):
    vector_x = df.drop(df.columns[-1], axis=1)  # Eliminar la última columna (etiquetas)
    vector_y = df[df.columns[-1]]               # Extraer solo la última columna (etiquetas)
    return vector_x, vector_y

# Separación de características y etiquetas
vector_x, vector_y = separate_dataframe(df)

# Selección de características numéricas
vector_x = vector_x.select_dtypes(include=['int64', 'float64'])

# Impresión de los vectores de características y etiquetas
print("\n","*"*50)
print(f"Vector de entrada: ")
print("*"*50)
print(vector_x.head())

print("\n","*"*50)
print(f"Vector de salida: ")
print("*"*50)
print(vector_y.head(), end="\n\n")

# Definición del clasificador de distancia mínima
def min_distance_classifier(train_x, train_y, test_x):
    # Calcula la media de cada clase
    class_means = train_x.groupby(train_y).mean()

    # Clasifica cada muestra en el conjunto de prueba
    predicted_y = []
    for _, row in test_x.iterrows():
        min_dist = float('inf')  # Inicialización de la distancia mínima
        min_class = None
        for cls, mean in class_means.iterrows():
            dist = np.linalg.norm(row - mean)  # Cálculo de la distancia euclidiana
            if dist < min_dist:
                min_dist = dist
                min_class = cls
        predicted_y.append(min_class)
    return predicted_y

# Definición del clasificador KNN
def knn_classifier(train_x, train_y, test_x, k=1):
    predicted_y = []
    for _, test_row in test_x.iterrows():
        distances = np.linalg.norm(train_x - test_row, axis=1)  # Distancia a cada punto de entrenamiento
        nearest_neighbors = np.argsort(distances)[:k]           # Índices de los k vecinos más cercanos
        votes = train_y.iloc[nearest_neighbors].mode()         # Votación mayoritaria
        predicted_y.append(votes.values[0])
    return predicted_y

# Definición de la función para dividir los datos en conjuntos de entrenamiento y prueba
def train_test_split(data_x, data_y, test_size=0.2):
    test_indices = np.random.choice(data_x.index, size=int(len(data_x) * test_size), replace=False)
    train_x = data_x.drop(test_indices)
    train_y = data_y.drop(test_indices)
    test_x = data_x.loc[test_indices]
    test_y = data_y.loc[test_indices]
    return train_x, train_y, test_x, test_y

# Función para evaluar el modelo
def evaluate_model(classifier, data_x, data_y, test_size=0.2):
    train_x, train_y, test_x, test_y = train_test_split(data_x, data_y, test_size)
    predicted_y = classifier(train_x, train_y, test_x)
    accuracy = sum(predicted_y == test_y) / len(test_y)
    error_rate = 1 - accuracy
    return accuracy, error_rate

# Función para la validación cruzada k-fold
def k_fold_cross_validation(classifier, data_x, data_y, k=5):
    fold_size = int(len(data_x) / k)
    accuracies = []
    for i in range(k):
        test_indices = range(i * fold_size, (i + 1) * fold_size)
        train_indices = list(set(range(len(data_x))) - set(test_indices))
        train_x, train_y = data_x.iloc[train_indices], data_y.iloc[train_indices]
        test_x, test_y = data_x.iloc[test_indices], data_y.iloc[test_indices]
        predicted_y = classifier(train_x, train_y, test_x)
        accuracy = sum(predicted_y == test_y) / len(test_y)
        accuracies.append(accuracy)
    mean_accuracy = np.mean(accuracies)
    error_rate = 1 - mean_accuracy
    return mean_accuracy, error_rate

# Función para la validación mediante bootstrap
def bootstrap_validation(classifier, data_x, data_y, n_iterations=100, sample_size=None):
    if sample_size is None:
        sample_size = len(data_x)
    accuracies = []
    for _ in range(n_iterations):
        sample_indices = np.random.choice(data_x.index, size=sample_size, replace=True)
        out_of_bag_indices = list(set(data_x.index) - set(sample_indices))
        train_x, train_y = data_x.loc[sample_indices], data_y.loc[sample_indices]
        test_x, test_y = data_x.loc[out_of_bag_indices], data_y.loc[out_of_bag_indices]
        predicted_y = classifier(train_x, train_y, test_x)
        accuracy = sum(predicted_y == test_y) / len(test_y)
        accuracies.append(accuracy)
    mean_accuracy = np.mean(accuracies)
    error_rate = 1 - mean_accuracy
    return mean_accuracy, error_rate

# Ejecución y evaluación del clasificador de distancia mínima
def run_min_distance_model(vector_x, vector_y):
    accuracy, error_rate = evaluate_model(min_distance_classifier, vector_x, vector_y, test_size=0.2)
    print("\n","="*50)
    print("Min Distance Classifier - Train Test Split")
    print("Accuracy:", accuracy, "Error Rate:", error_rate)
    
    accuracy, error_rate = k_fold_cross_validation(min_distance_classifier, vector_x, vector_y, k=5)
    print("\n","="*50)
    print("Min Distance Classifier - K-fold Cross Validation")
    print("Accuracy:", accuracy, "Error Rate:", error_rate)

    accuracy, error_rate = bootstrap_validation(min_distance_classifier, vector_x, vector_y, n_iterations=100)
    print("\n","="*50)
    print("Min Distance Classifier - Bootstrap")
    print("Accuracy:", accuracy, "Error Rate:", error_rate, end="\n\n")

# Ejecución y evaluación del clasificador KNN
def run_knn_model(vector_x, vector_y):
    accuracy, error_rate = evaluate_model(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, test_size=0.2)
    print("\n","="*50)
    print("KNN Classifier (K=1) - Train Test Split")
    print("Accuracy:", accuracy, "Error Rate:", error_rate)
    
    accuracy, error_rate = k_fold_cross_validation(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, k=5)
    print("\n","="*50)
    print("KNN Classifier (K=1) - K-fold Cross Validation")
    print("Accuracy:", accuracy, "Error Rate:", error_rate)
    
    accuracy, error_rate = bootstrap_validation(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, n_iterations=100)
    print("\n","="*50)
    print("KNN Classifier (K=1) - Bootstrap")
    print("Accuracy:", accuracy, "Error Rate:", error_rate, end="\n\n")

# Ejecución de los modelos con los vectores de características y etiquetas
run_min_distance_model(vector_x, vector_y)
run_knn_model(vector_x, vector_y)
