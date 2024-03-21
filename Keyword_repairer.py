#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:22:43 2024

@author: pmchozas
"""

import json
import os

from translation_class import get_source_identifiers





def write_json_file(file_path,data):
    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
def user_corrector(texto_original, texto_traducido, terminos,key):
    '''
    La mayoría de las veces no se ha traducido
    :param texto_original:
    :param texto_traducido:
    :param terminos:
    :return:
    '''
    print("-*********************")
    print("Texto:")
    print(texto_original)
    print("Texto:")
    print(texto_traducido)
    final_term=''
    print("Lista de términos:",terminos)
    print("Keyword a traducir:: ",key)
    # Calcular cuántas veces aparece cada término en el texto
    apariciones = {termino: texto_traducido.count(termino) for termino in terminos}

    print("Número de apariciones de cada término:")
    counter=1
    for termino, aparicion in apariciones.items():
        print(f"{counter}*{termino}: {aparicion}")
        counter=counter+1

    while True:
        opcion = input("Elige una opción (1 para el primer término, 2 para el segundo, 3 para el término original{"+str(key)+"}.  4 para escribir uno específico): ")

        if opcion == '1':
            termino = terminos[0]
            final_term=termino
            print(f"\nTérmino seleccionado: {termino}")
            print(f"El término '{termino}' aparece {texto_traducido.count(termino)} veces en el texto.")
            break
        if opcion == '2':
            termino = terminos[1]
            final_term=termino
            print(f"\nTérmino seleccionado: {termino}")
            print(f"El término '{termino}' aparece {texto_traducido.count(termino)} veces en el texto.")
            break
        if opcion == '3':
            termino = key
            final_term=termino
            print(f"\nTérmino seleccionado: {termino}")
            print(f"El término '{termino}' aparece {texto_traducido.count(termino)} veces en el texto.")
            break

        elif opcion == '4':
            termino_elegido = input("Introduce el término que deseas introducir: ")
            final_term = termino_elegido
            print(f"\nTérmino seleccionado: {termino_elegido}")
            print(f"El término '{termino_elegido}' aparece {texto_traducido.count(termino_elegido)} veces en el texto.")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")
    print('Final term',final_term, "\n\n\n")
    return final_term




InputPath = 'datasets/doc_translations/SemEval2017_GTranslate/'
OutputPath = 'datasets/doc_translations/SemEval2017_GTranslateReviewed/'
InputPath =  'datasets/doc_translations/OpenAI/SemEval2017_2/'
OutputPath = 'datasets/doc_translations/OpenAI/SemEval2017_2Reviewed/'
sourcedocs = os.listdir(InputPath)
targetdocs = os.listdir(OutputPath)
source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs)

### START
for ident in source_identifiers:

    if ident in target_identifiers:
        continue

    filepath=InputPath +str(ident)+ ".json"
    with open(filepath, 'r') as file:
        # data = file.read()
        data_dict = json.load(file)
        if data_dict['error_count'] == 0:
            a=0
            #TODO, WRITE FILE
        else:
            #print(data_dict['keys'].keys())
            num_errors = data_dict['error_count']
            print(ident,num_errors)

            for key in data_dict['keys'].keys():
                translation=data_dict['keys'][key]['translated_key']
                #if isinstance(translation, list): ## si es una lista, osea un error
                if translation=='':
                    #print(translation,key )
                    print(ident)
                    #new_term=user_corrector(data_dict['original_text'],data_dict['original_translation'],translation,key)
                    new_term = user_corrector(data_dict['original_text'], data_dict['original_translation'],data_dict['keys'][key]['error'][0], key)

                    num_errors=num_errors-1

                    data_dict['keys'][key]['translated_key']=new_term

            data_dict['error_count']=num_errors
            write_json_file(OutputPath +str(ident)+ ".json",data_dict)
            #cuando term
            #print('ERROR in',ident, data_dict['error_count'])




