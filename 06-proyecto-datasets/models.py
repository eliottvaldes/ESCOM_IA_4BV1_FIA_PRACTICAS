from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
datasets = {
    "Eliot": 53, # Iris
    "Ethel": 728, # 
    "Leo": 878, # Cirrhosis
    "Adair": 109, # Wine
}

dataset = fetch_ucirepo(id=datasets["Eliot"])
# obtenemos los datos
X = dataset.data.features 
y = dataset.data.targets 
df = pd.DataFrame(X, columns=dataset.data.feature_names)
df['target'] = y

df = df.dropna()

def separate_dataframe(df):
    vector_x = df.drop(df.columns[-1], axis=1) 
    vector_y = df[df.columns[-1]]
    return vector_x, vector_y


vector_x, vector_y = separate_dataframe(df)
vector_x = vector_x.select_dtypes(include=['int64', 'float64'])

print("\n","*"*50)
print(f"Vector de entrada: ")
print("*"*50)
print(vector_x.head())

print("\n","*"*50)
print(f"Vector de salida: ")
print("*"*50)
print(vector_y.head(), end="\n\n")

# MODELOS
def min_distance_classifier(train_x, train_y, test_x):
    # Calcular el promedio de cada clase en el conjunto de entrenamiento
    class_means = train_x.groupby(train_y).mean()

    # Clasificar cada observación en el conjunto de prueba
    predicted_y = []
    for _, row in test_x.iterrows():
        min_dist = float('inf')
        min_class = None
        for cls, mean in class_means.iterrows():
            dist = np.linalg.norm(row - mean)
            if dist < min_dist:
                min_dist = dist
                min_class = cls
        predicted_y.append(min_class)

    return predicted_y

def knn_classifier(train_x, train_y, test_x, k=1):
    predicted_y = []
    for _, test_row in test_x.iterrows():
        # Calcular la distancia a cada punto en el conjunto de entrenamiento
        distances = np.linalg.norm(train_x - test_row, axis=1)
        # Obtener los índices de los k vecinos más cercanos
        nearest_neighbors = np.argsort(distances)[:k]
        # Votación mayoritaria
        votes = train_y.iloc[nearest_neighbors].mode()
        predicted_y.append(votes.values[0])

    return predicted_y

# METODOS DE VALIDACION
def train_test_split(data_x, data_y, test_size=0.2):
    test_indices = np.random.choice(data_x.index, size=int(len(data_x) * test_size), replace=False)
    train_x = data_x.drop(test_indices)
    train_y = data_y.drop(test_indices)
    test_x = data_x.loc[test_indices]
    test_y = data_y.loc[test_indices]
    return train_x, train_y, test_x, test_y

def evaluate_model(classifier, data_x, data_y, test_size=0.2):
    train_x, train_y, test_x, test_y = train_test_split(data_x, data_y, test_size)
    predicted_y = classifier(train_x, train_y, test_x)
    accuracy = sum(predicted_y == test_y) / len(test_y)
    error_rate = 1 - accuracy
    return accuracy, error_rate



def k_fold_cross_validation(classifier, data_x, data_y, k=5):
    fold_size = int(len(data_x) / k)
    accuracies = []
    for i in range(k):
        # Dividir los datos en folds
        test_indices = range(i * fold_size, (i + 1) * fold_size)
        train_indices = list(set(range(len(data_x))) - set(test_indices))

        train_x, train_y = data_x.iloc[train_indices], data_y.iloc[train_indices]
        test_x, test_y = data_x.iloc[test_indices], data_y.iloc[test_indices]

        # Evaluar el clasificador
        predicted_y = classifier(train_x, train_y, test_x)
        accuracy = sum(predicted_y == test_y) / len(test_y)
        accuracies.append(accuracy)

    mean_accuracy = np.mean(accuracies)
    error_rate = 1 - mean_accuracy
    return mean_accuracy, error_rate


def bootstrap_validation(classifier, data_x, data_y, n_iterations=100, sample_size=None):
    if sample_size is None:
        sample_size = len(data_x)

    accuracies = []
    for _ in range(n_iterations):
        # Crear un conjunto de entrenamiento con muestreo con reemplazo
        sample_indices = np.random.choice(data_x.index, size=sample_size, replace=True)
        out_of_bag_indices = list(set(data_x.index) - set(sample_indices))

        train_x, train_y = data_x.loc[sample_indices], data_y.loc[sample_indices]
        test_x, test_y = data_x.loc[out_of_bag_indices], data_y.loc[out_of_bag_indices]

        # Evaluar el clasificador
        predicted_y = classifier(train_x, train_y, test_x)
        accuracy = sum(predicted_y == test_y) / len(test_y)
        accuracies.append(accuracy)

    mean_accuracy = np.mean(accuracies)
    error_rate = 1 - mean_accuracy
    return mean_accuracy, error_rate


# USO DE LOS MODELOS
## 4 => MODELO: DISTANCIA MINIMA
### 4.A => DISTANCIA MINIMA - EVALUADO CON: TRAIN-TEST SPLIT
accuracy, error_rate = evaluate_model(min_distance_classifier, vector_x, vector_y, test_size=0.2)
print("\n","="*50)
print("Min Distance Classifier - Train Test Split")
print("Accuracy:", accuracy, "Error Rate:", error_rate)


### 4.B => DISTANCIA MINIMA - EVALUADO CON: K FOLD CROSS VALIDATION
accuracy, error_rate = k_fold_cross_validation(min_distance_classifier, vector_x, vector_y, k=5)
print("\n","="*50)
print("Min Distance Classifier - K-fold Cross Validation")
print("Accuracy:", accuracy, "Error Rate:", error_rate)

### 4.C => DISTANCIA MINIMA - EVALUADO CON: BOOTSTRAP
accuracy, error_rate = bootstrap_validation(min_distance_classifier, vector_x, vector_y, n_iterations=100)
print("\n","="*50)
print("Min Distance Classifier - Bootstrap")
print("Accuracy:", accuracy, "Error Rate:", error_rate)


## 5 => MODELO: KNN(K=1)
### 5.A => KNN - EVALUADO CON: TRAIN-TEST SPLIT
accuracy, error_rate = evaluate_model(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, test_size=0.2)
print("\n","="*50)
print("KNN Classifier (K=1) - Train Test Split")
print("Accuracy:", accuracy, "Error Rate:", error_rate)

### 5.B => KNN - EVALUADO CON: K FOLD CROSS VALIDATION
accuracy, error_rate = k_fold_cross_validation(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, k=5)
print("\n","="*50)
print("KNN Classifier (K=1) - K-fold Cross Validation")
print("Accuracy:", accuracy, "Error Rate:", error_rate)

### 5.C => KNN - EVALUADO CON: BOOTSTRAP
accuracy, error_rate = bootstrap_validation(lambda x, y, z: knn_classifier(x, y, z, k=1), vector_x, vector_y, n_iterations=100)
print("\n","="*50)
print("KNN Classifier (K=1) - Bootstrap")
print("Accuracy:", accuracy, "Error Rate:", error_rate)