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
import os
from collections import Counter


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
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text


def translate_text_helsinki(text, source_language, target_language):

    # Load translation pipeline
    translation_pipeline = pipeline(task="translation", model=f"Helsinki-NLP/opus-mt-{source_language}-{target_language}")

    # Translate text
    translated_text = translation_pipeline(text)[0]['translation_text']
    return translated_text

def replace_with_quotes(text, term):
    #\b Matches the empty string, but only at the beginning or end of a word. A word is defined as a sequence of word characters. Note that formally, \b is defined as the boundary between a \w and a \W character (or vice versa), or between \w and the beginning or end of the string. This means that r'\bat\b' matches 'at', 'at.', '(at)', and 'as at ay' but not 'attempt' or 'atlas'.

    pattern = r'\b' + re.escape(term) + r'\b'
    newterm=f'"{term}"'

    replaced_text = re.sub(pattern, newterm, text)
    print(pattern)
    print(newterm)
    print("original term quoted")
    print(replaced_text)
    return replaced_text        

def read_term_list_file(filepath):
    lst = []
    with open(filepath, "r", encoding='utf-8') as f:
        for line in f:
            k=line
            k = k.strip()
            lst.append(k)
    return lst


def read_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
             lines = [line.strip() for line in file.readlines()]

        return lines
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al intentar leer el archivo '{file_path}': {e}")
        return None

def read_file_content(path):
    with open(path, 'r') as file:
        text = file.read().replace('\n', ' ')
    return text

def extract_quoted_terms(text):
    # Usamos una expresión regular para encontrar los términos entre comillas
    quoted_terms = re.findall(r'"([^"]+)"', text)
    print('quted terms ')
    print(quoted_terms)
    return quoted_terms
#son todos iguales
def detect_different_translations(lista):
    # Verifica si la lista está vacía
    if len(lista) == 0:
        return False
    # Compara todos los elementos de la lista con el primero
    return all(elemento.lower() == lista[0].lower() for elemento in lista)



#de las traducciones diferentes, coge las que mayor número presenten. si son diferentes, coge el primero
def most_repeated_element(lst):
    # Count occurrences of each element in the list
    counts = Counter(lst)
    
    # Find the most common element(s)
    most_common = counts.most_common(1)
    
    # If there are ties for the most common element, return all of them
    max_count = most_common[0][1]
    most_repeated=[]

    #most_repeated = [element for element, count in counts.items() if count == max_count]
    for element, count in counts.items():
    # Check if the count of the current element is equal to the maximum count
      if count == max_count:
          # If yes, add the element to the most_repeated list
          most_repeated.append(element)
          
          return most_repeated
          if not most_repeated: 
              return lst[0]
                


class Translation():
    def __init__(self, text, keys):
        self.original_text=text #original text
        self.original_keys=keys #original keywords
        self.original_translation="" 
        self.translated_annotated_text=[]# lista con tantos textos como keywords haya
        self.translated_keywords=[] #después 
        self.errors=[] #si alguna traducción es diferente
        self.error_count=0
        self.id=""
        self.annotated_sentence = []

    def generate_annotated_sentences(self):
        self.annotated_sentence = []
        for key in self.original_keys:
            cleankey = re.sub(r'[\'"‘’]', '', key)
            self.annotated_sentence.append(replace_with_quotes(self.original_text, cleankey))
            
        return self.annotated_sentence
    def compare_annotated_keywords(self):
        for k in self.translated_annotated_text:
            extracted=extract_quoted_terms(k)
            print(extracted)
            if detect_different_translations(extracted): 
                print('ok')
                self.translated_keywords.append(extracted[0])  
                self.errors.append("")
            else:
                print('error', extracted)
                self.errors.append((extracted))
                self.error_count+=1
                self.translated_keywords.append(extracted)
    def write_json(self, PathTrans):
        data = {
            "original_text" : self.original_text ,
            "original_translation": self.original_translation ,
            "error_count": self.error_count ,
            "keys":{}
            }
        counter=0
        for key in self.original_keys:
            cleankey = re.sub(r'[\'"‘’“”]', '', key)
            data['keys'][cleankey]={
                    "translated_key": self.translated_keywords[counter],
                    "translated_annotated_text": self.translated_annotated_text[counter],
                    "error":self.errors[counter]
                   }
            counter+=1

            
        file_path = PathTrans+"/"+self.id+".json"

        # Write data to the JSON file
        with open(file_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(self.id + '.json saved')

        
            


# PathDocs= 'datasets/source/SemEval2017/docsutf8/S030193221400144X.txt'
# PathKeys= 'datasets/source/SemEval2017/keys/S030193221400144X.key'

# text=read_file_content(PathDocs)
# keys=read_term_list_file(PathKeys)






# extract=extract_quoted_terms("hola mundo qué tal \"mundo\"")
# print(extract)