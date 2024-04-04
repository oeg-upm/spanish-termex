from transformers import MarianMTModel, MarianTokenizer, BertTokenizer, BertModel
import torch
import ollama
prompt="""You are a translator of English to Spanish specialized in terms and HTML tags. You will recieve a text in English with a term marked between the HTML tag <br> and </br>. In Output1, you generate the full translation of the text. In Output2, you give the translation of the term that was between HTML tags. Some examples:
Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
Output1: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de computación móvil."
Output2: "computación móvil".
Input: "Where have all the <br>PC makers</br> gone?".
Output1: "¿Dónde se han ido todos los fabricantes de PC?".
Output2: "fabricantes de PC".
Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail".
Output1: "El papel del enredo cuántico del estado inicial se discute en detalle".
Output2: "estado inicial".
Input: "A second goal is to describe how this topic fits into the even larger field of MR methods and concepts-in particular, making ties to topics such as wavelets and <br>multigrid methods</br>".
Output1: "Un segundo objetivo es describir cómo este tema se relaciona con el campo más amplio de métodos y conceptos de MR -en particular, estableciendo vínculos con temas como wavelets y métodos multigrid".
Output2: "métodos multigrid"
Now. For this text:
"""



Lista=["S0098300414002532","S1361841516300822","S0301679X13003289","S2212667812000780","S0927025614006181","S0379711215000223","S2352179114200032","S0038092X15000559","S092702561300267X","S0370269302011838","S0305440314001927","S0301679X14000449","S2212671612000741","S2352179114200032","S0379711215000223","S0927025614006181","S0301679X13003289","S2212667812000780","S1361841516300822","S0098300414002532"]

print(len(Lista))
import os
import json
import shutil
def borrar_archivos_con_nombre_en_lista(carpeta, lista_nombres,carpeta_dest):
    for nombre_archivo in os.listdir(carpeta):
        n_name= nombre_archivo.replace(".json",'')
        if n_name in lista_nombres:
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            #os(ruta_archivo)
            print(f"Archivo {nombre_archivo} copiado.")
            ruta_destino = os.path.join(carpeta_dest, nombre_archivo)
            shutil.copyfile(ruta_archivo, ruta_destino)
            with open(ruta_archivo, 'r') as file:
                # data = file.read()
                data_dict = json.load(file)
                print(data_dict['error_count'])

OutputPath = 'datasets/doc_translations/OpenAI/SemEval2017/'
OutputPath2 = 'datasets/doc_translations/OpenAI/SemEval2017_2/'

#borrar_archivos_con_nombre_en_lista(OutputPath, Lista,OutputPath2)


from collections import Counter

def most_repeated_value(lst):
    # Count occurrences of each element in the list
    counts = Counter(lst)
    # Get the most common element and its count
    most_common = counts.most_common(1)
    # Return the most common element
    return most_common[0][0] if most_common else None


my_list = [1, 2, 3, 3, 3, 4, 4, 5, 5, 5, 5]
my_list = [1,2]
result = most_repeated_value(my_list)
print("Most repeated value:", result)