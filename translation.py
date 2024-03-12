#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 19:51:02 2024

@author: pmchozas
"""

import os
from translation_class import read_lines,read_file_content,Translation,translate_text_google
from googletrans import Translator
import re
import json
import httpx

#PathDocs = 'datasets/source/SemEval2017/docsutf8'
PathDocs='datasets/doc_translations/problematico'
PathKeys = 'datasets/source/SemEval2017/keys'
#PathTrans = 'datasets/doc_translations/GTranslate'
PathTrans = 'datasets/doc_translations/testingproblematico'
# PathDocs='datasets/translation_test/docsutf8'
# PathKeys='datasets/translation_test/keys'
# PathTrans='datasets/translation_test/trans'


sourcedocs = os.listdir(PathDocs)
sourcekeys = os.listdir(PathKeys)
transdocs = os.listdir(PathTrans)

notrans = []

source_language = "en"  # English
target_language = "es"

file_no_ds = [archivo for archivo in sourcedocs if not archivo.endswith('.DS_Store')]


for s in file_no_ds:
    #print(s)
    pos = s.find('.')
    subs = s[:pos]
    trans = subs + '.json'
    if trans not in transdocs:
        notrans.append(s)

for t in notrans:
    pos = t.find('.')
    subs = t[:pos]
    key = subs + '.key'
    print(t)
    readdoc = read_file_content(PathDocs + '/' + t)
    cleandoc = re.sub(r'[\'"‘’“”]', '', readdoc)
    

    if key in sourcekeys:
        readkey = read_lines(PathKeys + '/' + key)
        translation = Translation(cleandoc, readkey)
        cleandoc=translation.original_text
        translation.id = subs
        list_annotations = translation.generate_annotated_sentences()
        print(list_annotations)
        translation.original_translation = translate_text_google(cleandoc, src_lang='en', dest_lang='es')
        for annotated in list_annotations:
            tr = translate_text_google(annotated, src_lang='en', dest_lang='es')
            print(tr)
            translation.translated_annotated_text.append(tr)

        translation.compare_annotated_keywords()
        translation.write_json(PathTrans)

#READ FILE
'''

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
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al intentar leer el archivo '{file_path}': {e}")
        return None

PathDocs= 'datasets/source/SemEval2010/docsutf8'
PathKeys= 'datasets/source/SemEval2010/keys'
PathTrans= 'datasets/translations'
id= 'S0003491613001516'

#CHECK REMAINING TRANSLATED FILES


sourcefiles = os.listdir(PathKeys)
transfiles = os.listdir(PathTrans)
notrans=[]
for s in sourcefiles:
    pos=s.find('.')
    subs=s[:pos]
    trans=subs+'.keytrans.json'
    if trans not in transfiles:
        notrans.append(s)
print(notrans)


#IMPORT GOOGLE TRANSLATE
#timeout = httpx.Timeout(5) # 5 seconds timeout
def translate_text_google(text, src_lang='en', dest_lang='es'):
    timeout = httpx.Timeout(20) # 5 seconds timeout
    translator = Translator(timeout=timeout)
    #translator = Translator()
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text

def main():
    # Texto en inglés
    text_to_translate = "Hello, how are you? This is an example text."

    # Traducir el texto de inglés a español
    translated_text = translate_text_google(text_to_translate)
    print("Texto traducido al español:")
    print(translated_text)

    # Término específico para comprobar la traducción
    term_to_check = "example"
    translation_of_term = translate_text_google(term_to_check)
    print(f"La traducción de '{term_to_check}' al español es: {translation_of_term}")

if __name__ == "__main__":
    main()
    
    
#ADD TERM MARKER
    
def replace_with_quotes(text, term):
    replaced_text = text.replace(term, f'"{term}"')
    return replaced_text


def extract_quoted_terms(text):
    # Usamos una expresión regular para encontrar los términos entre comillas
    quoted_terms = re.findall(r'"([^"]*)"', text)
    return quoted_terms
def remove_quotes_from_term(text):
    # Usamos una expresión regular para encontrar términos entre comillas y los quitamos

    text_without_quotes = text.replace('"', '')
    #text_without_quotes = re.sub(r'<span>([^"]*)<span>', r'\1', text)
    return text_without_quotes


def translate_keyword(key,text,translation_list):
  replaced_text= replace_with_quotes(text,key)

  print(replaced_text)
  translated=translate_text_google(replaced_text)
  #translated=translate_text_helsinki(replaced_text, source_language, target_language)
  #translated=translate_text_mariaNMT(text)
  translation_list.append(remove_quotes_from_term(translated))
  #print(translated)
  res= extract_quoted_terms(translated)
  #print(res)
  dictionary = dict(enumerate(set(res)))
  #print(dictionary)
  length = len(dictionary)
  if length>1:
    print('fatal error')
    print(translated)
    print(res)


translation_list= []
#for key in keys:
#    translate_keyword(key,doc,translation_list)


len(translation_list)

translation_list
dictionary = dict(enumerate(set(translation_list)))
#print(dictionary)
length = len(dictionary)


#TRANSLATE ALL KEYS AND SAVE IN DICTIONARIES
keys = os.listdir(PathKeys)

folder_path='datasets/translations/'
for key in notrans:
  readkey=read_lines(PathKeys+'/'+key)
  print(key)
  trans_dict={}
  dict_file=key+'trans.json'
  dict_path=os.path.join(folder_path, dict_file)
  for k in readkey:
    try:
      print(k)
      translated=translate_text_google(k)
      print(translated)
      trans_dict[k]=translated
    except TypeError:
      print("TypeError: None")
  #print(trans_dict)
  with open(dict_path, 'w', encoding='utf-8') as file:
    json.dump(trans_dict, file, ensure_ascii=False)
    
'''

