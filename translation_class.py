#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:48:38 2024

@author: pmchozas
"""
import transformers
from transformers import pipeline
import re
import httpx
from googletrans import Translator
import json
from transformers import MarianMTModel, MarianTokenizer

def translate_text_mariaNMT(text):
    model_name = "Helsinki-NLP/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    #print(tokenizer.supported_language_codes)
    model = MarianMTModel.from_pretrained(model_name)
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    result=[tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return(result[0])

def translate_text_google(text, src_lang='en', dest_lang='es'):
    timeout = httpx.Timeout(20) # 5 seconds timeout
    translator = Translator(timeout=timeout)
    translator.raise_Exception = True
    #translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text


def translate_text_helsinki(text, source_language, target_language):

    # Load translation pipeline
    translation_pipeline = pipeline(task="translation", model=f"Helsinki-NLP/opus-mt-{source_language}-{target_language}")

    # Translate text
    translated_text = translation_pipeline(text)[0]['translation_text']
    return translated_text

def replace_with_quotes(text, term):
    replaced_text = text.replace(term, f'"{term}"')
    return replaced_text        

def read_term_list_file(filepath):
    lst = []
    with open(filepath, "r", encoding='utf-8') as f:
        for line in f:
            k=line
            k = k.strip()
            lst.append(k)
    return lst

def read_file_content(path):
    with open(path, 'r') as file:
        text = file.read().replace('\n', '')
    return text

def extract_quoted_terms(text):
    # Usamos una expresión regular para encontrar los términos entre comillas
    quoted_terms = re.findall(r'"([^"]*)"', text)
    return quoted_terms
#son todos iguales
def detect_different_translations(lista):
    # Verifica si la lista está vacía
    if len(lista) == 0:
        return False
    # Compara todos los elementos de la lista con el primero
    return all(elemento == lista[0] for elemento in lista)
#de las traducciones diferentes, coge las que mayor número presenten. si son diferentes, coge el primero
def get_best_match(lista):

    matches = {}
    
    # Iterar sobre cada elemento de la lista
    for item in lista:
        # Si el elemento ya está en el diccionario, significa que hemos encontrado una coincidencia
        if item in matches:
            return item
        else:
            return lista[0]
            


class Translation():
    def __init__(self, text, keys):
        self.original_text=text #original text
        self.original_keys=keys #original keywords
        self.original_translation="" 
        self.translated_annotated_text=[]# lista con tantos textos como keywords haya
        self.translated_keywords=[] #después 
        self.errors=[] #si alguna traducción es diferente
        self.error_count=0
    def generate_annotated_sentences(self):
        self.annotated_sentence=[]
        for key in self.original_keys:
            self.annotated_sentence.append(replace_with_quotes(self.original_text, key))
        return self.annotated_sentence
    def compare_annotated_keywords(self):
        for k in self.translated_annotated_text:
            extracted=extract_quoted_terms(k)
            print(extracted)
            if detect_different_translations(extracted): 
                print('ok')
                self.translated_keywords.append(extracted[0])
                
            else:
                print('error', extracted)
                self.errors.append('error in ' + str(extracted))
                self.error_count+=1
                self.translated_keywords.append(get_best_match(extracted))
            


PathDocs= 'datasets/source/SemEval2017/docsutf8/S030193221400144X.txt'
PathKeys= 'datasets/source/SemEval2017/keys/S030193221400144X.key'

text=read_file_content(PathDocs)
keys=read_term_list_file(PathKeys)

translation=Translation(text, keys)
list_annotations=translation.generate_annotated_sentences()

source_language = "en"  # English
target_language = "es"

for annotated in list_annotations: 
    tr=translate_text_google(annotated, src_lang='en', dest_lang='es')
    print(tr)
    translation.translated_annotated_text.append(tr)
   
translation.compare_annotated_keywords()    


data = {
    "original_text" : translation.original_text ,
    "original_translation": translation.original_translation , 
    "error_count": translation.error_count ,
    "errors":translation.errors ,
    
    }
counter=0
for key in translation.original_keys:
    data[key]={
            "translated_key": translation.translated_keywords[counter],
            "translated_annotated_text": translation.translated_annotated_text[counter],
           }
    counter+=1

    
file_path = "datasets/source/data.json"

# Write data to the JSON file
with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)



# extract=extract_quoted_terms("hola mundo qué tal \"mundo\"")
# print(extract)