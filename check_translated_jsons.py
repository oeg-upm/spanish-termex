#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:22:43 2024

@author: pmchozas
"""

import json
import os

PathTrans = 'datasets/doc_translations/GTranslate'
transdocs = os.listdir(PathTrans)

file_no_ds = [archivo for archivo in transdocs if not archivo.endswith('.DS_Store')]

'''
#borrar archivos con errores
for t in file_no_ds:
# Abre el archivo JSON
    print(t)
    filepath=PathTrans + "/" + t
    with open(filepath, 'r+') as file:
        # data = file.read()
        data_dict = json.load(file)
        if data_dict['error_count'] != 0: 
            os.remove(filepath)
 '''

NewPath='datasets/doc_translations/nuevos'
     
for t in file_no_ds:
# Abre el archivo JSON
    print(t)
    filepath=PathTrans + "/" + t
    newfile=NewPath+"/"+t
    with open(filepath, 'r') as file:
        data_dict = json.load(file)
        if 'errors' in data_dict:
            del data_dict['errors']
            for k in data_dict['keys']:
                data_dict['keys'][k]['errors']=""
        print(data_dict)
        with open(newfile, 'w', encoding='utf-8') as archivo:
            json.dump(data_dict, archivo,ensure_ascii=False, indent=4)



