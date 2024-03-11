

import os
import json

def contar_errores_en_carpeta(ruta_carpeta):
    # Contador para llevar la cuenta de los archivos con error
    archivos_con_error = 0

    # Iterar sobre todos los archivos en la carpeta
    for nombre_archivo in os.listdir(ruta_carpeta):
        # Comprobar si el archivo es un archivo JSON
        if nombre_archivo.endswith('.json'):
            # Construir la ruta completa al archivo
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

            # Leer el archivo JSON
            with open(ruta_completa, 'r') as archivo:
                datos_json = json.load(archivo)

            '''TODO'''
            # Verificar si el campo 'error' tiene más de un caracter


    return archivos_con_error

# Ruta a la carpeta que contiene los archivos JSON
ruta_carpeta_json = 'ruta/a/la/carpeta'

# Llamar a la función para contar los archivos con error
archivos_con_error = contar_errores_en_carpeta(ruta_carpeta_json)

# Imprimir el resultado
print(f"Total de archivos con error: {archivos_con_error}")