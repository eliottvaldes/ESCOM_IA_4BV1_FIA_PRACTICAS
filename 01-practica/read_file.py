""" 
Funcion para leer archivo dado un path inicial
 """

 def read_file(path_file):
    with open(path_file, 'r') as file:
        return file.read()
