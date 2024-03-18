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
#from googletrans import Translator
import json
from transformers import MarianMTModel, MarianTokenizer
import os
from collections import Counter
import nltk
nltk.download('punkt')
from googletrans import Translator


def separate_sentences(text):

    sentences = nltk.sent_tokenize(text)

    ## VERIFIER
    '''
    S1:"This method has been since extended by Conrad et al.",
    S2: "[34] to incorporate uncertainties in detector sensitivity and the background estimate based on an approach described by Cousins and Highland [35].",
    HAY QUE UNIR           
    '''
    new_sentences=[]
    var=''
    for i,sentence in enumerate(sentences):
        if i ==0:
            new_sentences.append(sentence)
            continue
        if sentence[0].isupper():
            if var !='':
                new_sentences.append(var.strip())
            var= sentence
            continue
        else:
            var=var+' '+sentence
    if var != '':
        new_sentences.append(var.strip())




    return new_sentences



def translate_texts_google(sentences, translated_sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = ""
    for sentence, t_sentence in zip(sentences,translated_sentences):

        if not is_sentence_to_translate(sentence):
            translated_text += t_sentence + " "
            continue

        # Agregar punto al final de la oración para tokenización
        sentence = sentence.strip()
        # Tokenizar y traducir la oración
        timeout = httpx.Timeout(20) # 5 seconds timeout
        translator = Translator(timeout=timeout)
        translator.raise_Exception = True
        translated_sentence = translator.translate(sentence, src='en', dest='es')

        # Agregar la oración traducida al texto traducido
        translated_text += translated_sentence.text + " "


    return translated_text



def translate_text_google(text, src_lang='en', dest_lang='es'):
    timeout = httpx.Timeout(20) # 5 seconds timeout
    translator = Translator(timeout=timeout)
    translator.raise_Exception = True
    translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated_text.text






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
        lines=[]
        with open(file_path, 'r', encoding='utf-8') as file:
             for line in file.readlines():
                text= clean_text(line)
                lines.append(text)


        return lines
    except FileNotFoundError:
        print(f"El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al intentar leer el archivo '{file_path}': {e}")
        return None

def read_file_content(path):
    with open(path, 'r') as file:
        text = file.read()
        text= clean_text(text)
    return text

def clean_text(text):
    text=  re.sub(r'[\'"‘’“”]', '', text)
    text=  text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('  ', ' ')
    text = text.replace("\u00A0", " ")


    return text.strip()

def is_sentence_to_translate(sentence):

    #if re.search(r'\uFFFC', sentence):
    if '<br>' in sentence:
        return True
    return False

import re

import re


def find_term(text, term):
    """
    Find occurrences of the term in the text, ensuring it's not part of a larger word and can appear with punctuation.

    Args:
    - text (str): The input text.
    - term (str): The term to search for.

    Returns:
    - matches (list): List of matches found in the text.
    """
    # Construct the regex pattern with word boundaries and optional punctuation
    pattern = re.compile(rf'\b{re.escape(term)}[.,]?\b')

    # Find all matches in the text
    matches = pattern.findall(text)
    return matches


def replace_with_quotes_h(text, term):
    """
    Annotate a term within a text with Zero Width Space characters.

    Args:
    - text (str): The input text.
    - term (str): The term to be annotated.

    Returns:
    - annotated_text (str): The text with the term annotated.
    """
    # Insert Zero Width Space characters before and after the term
    pattern = re.compile(rf'\b{re.escape(term)}[.,]?\b',re.IGNORECASE)
    newterm = "<br>" + term + "</br>"  # f'"{term}"'
    replaced_text = re.sub(pattern, newterm, text,re.IGNORECASE)
    #replaced_text = text.replace(term, "<br>" + term + "</br>")


    return replaced_text

def replace_with_quotes_hard(text, term):
    escaped_substring = re.escape(term)
    # Construct the regex pattern to find the substring
    pattern = '(' + escaped_substring + ')'
    newterm = "<br>" + term + "</br>"  # f'"{term}"'
    # Use re.sub() to replace the matched substring with annotated version
    replaced_text = re.sub(pattern, newterm, text,re.IGNORECASE)

    return replaced_text


def extract_quoted_terms_h(text):
    """
    Extract terms annotated with Zero Width Space characters from a text using regular expressions.

    Args:
    - text (str): The input text with annotated terms.

    Returns:
    - annotated_terms (list): List of terms extracted from the text.
    """
    # Define regular expression pattern to match terms between Zero Width Space characters
    pattern = re.compile(r'<br>(.+?)</br>')
    # Find all matches in the text
    annotated_terms = pattern.findall(text)
    return annotated_terms

def remove_quotes(sentence):
    sentence=sentence.replace('<br>','').replace('</br>','')
    return sentence

#text=                "<br>X-Rite</br>: más que una empresa de artes gráficas Aunque es bien conocido como fabricante de densitometros y espectrofotómetros, <br>X-Rite</br> está activo en la medición de luz y forma en muchas industrias."

#print(extract_quoted_terms_h(text))

# Output: example

# Test the functions

######## PATRI FUCTIONS
def replace_with_quotes(text, term):
    # \b Matches the empty string, but only at the beginning or end of a word. A word is defined as a sequence of word characters. Note that formally, \b is defined as the boundary between a \w and a \W character (or vice versa), or between \w and the beginning or end of the string. This means that r'\bat\b' matches 'at', 'at.', '(at)', and 'as at ay' but not 'attempt' or 'atlas'.

    pattern = r'\b' + re.escape(term) + r'\b'
    newterm = f'"{term}"'

    replaced_text = re.sub(pattern, newterm, text)

    return replaced_text
def extract_quoted_terms(text):
    # Usamos una expresión regular para encontrar los términos entre comillas
    pattern = re.compile(r'"([^"]+)"')
    quoted_terms = re.findall(pattern,text)     #"([^"]+)"

    return quoted_terms




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
    def __init__(self):
        self.original_text="" #original text
        self.original_keys=[] #original keywords
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
            self.annotated_sentence.append(replace_with_quotes(self.original_text, key))
            
        return self.annotated_sentence

    def generate_annotated_sentences_helsinki(self):
        self.annotated_sentence = []
        self.original_text_sentences= separate_sentences(self.original_text)
        for key in self.original_keys:
            annotated_text_sentences = self.original_text_sentences.copy()

            output_list = [replace_with_quotes(i, key) for i in annotated_text_sentences]
            self.annotated_sentence.append(output_list)

        return self.annotated_sentence
    def compare_annotated_keywords(self):
        for k in self.translated_annotated_text:
            extracted=extract_quoted_terms(k)
            #print(extracted)
            if detect_different_translations(extracted): 
                #print('ok')
                self.translated_keywords.append(extracted[0])  
                self.errors.append([""])
            else:
                #print('error', extracted)
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
            #cleankey = re.sub(r'[\'"‘’“”]', '', key)
            data['keys'][key]={
                    "translated_key": self.translated_keywords[counter],
                    "translated_annotated_text": self.translated_annotated_text[counter],
                    "error":self.errors[counter]
                   }
            counter+=1

            
        file_path = PathTrans+"/"+self.id+".json"

        # Write data to the JSON file
        with open(file_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        #print(self.id + '.json saved')



class Key():
    def __init__(self,term):
        self.key=term
        self.translated_term=''
        self.candidates=[]

        self.translated_annotated_text=''
        self.errors=[]
        self.original_annotated_sentences=[]
        self.translated_annotated_samples = []
        self.original_annotated_samples = []

        self.is_in_text = False

    def get_json(self):
        val= {
            "translated_key": self.translated_term,
            "is_in_text": self.is_in_text,
            "original_annotated_sentences":self.original_annotated_sentences,
            "original_annotated_samples": self.original_annotated_samples,
            "translated_annotated_samples": self.translated_annotated_samples,
            "translated_text": self.translated_annotated_text,
            "candidates":self.candidates,
            "error": self.errors
        }
        return val

    def check_annotations(self):
        for annot_sent in self.original_annotated_sentences:
            if is_sentence_to_translate(annot_sent):
                self.is_in_text = True
                return True

        return False


MAX_COUNTER=0

class TranslationH():
    def __init__(self, _id, text_, keys_):
        self.original_text = text_  # original text
        self.original_keys = keys_  # original keywords
        self.id = _id
        self.keys = []  # original keywords

        for k in self.original_keys:
            self.keys.append(Key(k))

        self.original_text_sentences = separate_sentences(self.original_text)



        self.translated_text = ""
        self.translated_text_sentences=[]

        #self.translated_annotated_text = []  # lista con tantos textos como keywords haya
        #self.translated_keywords = []  # después
        #self.errors = []  # si alguna traducción es diferente
        self.error_count = 0




    def generate_annotated_sentences(self):

        error=0
        for key in self.keys:#self.original_keys:
            annotated_text_sentences = self.original_text_sentences.copy()
            output_list = [replace_with_quotes_h(i, key.key) for i in annotated_text_sentences]
            key.original_annotated_sentences=output_list
            val= key.check_annotations()

            ## Validamos una primera vez y si no string matching
            if not val:
                output_list = [replace_with_quotes_hard(i, key.key) for i in annotated_text_sentences]
                key.original_annotated_sentences = output_list
                val=key.check_annotations()


            ## Validamos una segunda vez pasar a plural. SemEval2010
            if not val:
                plural_key= pluralize(key.key)

                output_list = [replace_with_quotes_hard(i, plural_key) for i in annotated_text_sentences]
                key.original_annotated_sentences = output_list
                val = key.check_annotations()
                if val:
                    print(self.id, key.key, '->', plural_key)
                    key.key = plural_key


            if not val:
                start, end, original_term = find_term_position(key.key, self.original_text)
                if original_term !=None:
                    output_list = [replace_with_quotes_h(i, original_term) for i in annotated_text_sentences]
                    key.original_annotated_sentences = output_list
                    val = key.check_annotations()

                    key.key = original_term


            if not val:
                #print("Error in>>> ",self.id,key.key)
                error=error+1



        return error

    def compare_annotated_keywords(self):
        for k in self.keys: #translated_annotated_text:
            extracted = extract_quoted_terms_h(k.translated_annotated_text)
            #print('>>>>',extracted)
            if detect_different_translations(extracted):
                #print('ok')
                k.translated_term= extracted[0]#elf.translated_keywords.append(extracted[0])
                k.errors.append([""])
            else:
                #print('error', extracted)
                k.errors.append(extracted)
                self.error_count += 1
                k.errors.append(extracted)



    def write_json(self, PathTrans):
        data = {
            "id":self.id,
            "original_text": self.original_text,
            "original_translation": self.translated_text,
            "original_sentences": self.original_text_sentences,
            "error_count": self.error_count,
            "keys": {}
        }

        for key in self.keys:
            data['keys'][key.key] = key.get_json()


        file_path = PathTrans + "/" + self.id + ".json"

        # Write data to the JSON file
        with open(file_path, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        #print(self.id + '.json saved')



def get_source_identifiers(file_list):
    identifiers=[]
    for file_ in file_list:
        if file_.endswith('.txt'):
            identifiers.append(file_.replace('.txt',''))
        if file_.endswith('.json'):
            identifiers.append(file_.replace('.json',''))

    return identifiers


def pluralize(word):

    # Reglas generales para la mayoría de las palabras
    if word.endswith('s') or word.endswith('sh') or word.endswith('ch') or word.endswith('x') or word.endswith('z'):
        return word + 'es'
    elif word.endswith('y') and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    else:
        return word + 's'



import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')


def find_term_position(term, text):
    """
    Encuentra la posición del término en el texto lematizado y recupera el término original.
    Devuelve la posición del término en el texto original y el término original.
    """
    # Tokenizar y lematizar el texto
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Lematizar el término
    term_tokens = word_tokenize(term)
    lemmatized_term = " ".join([lemmatizer.lemmatize(token) for token in term_tokens])

    # Buscar el término lematizado en el texto lematizado
    try:
        start_index = lemmatized_tokens.index(lemmatized_term.split()[0])
        end_index = start_index + len(term_tokens) - 1
        if lemmatized_tokens[start_index:end_index + 1] == lemmatized_term.split():
            original_term = " ".join(tokens[start_index:end_index + 1])
            return start_index, end_index, original_term
        else:
            return -1, -1, None  # Término no encontrado en el texto
    except ValueError:
        return -1, -1, None  # Término no encontrado en el texto

