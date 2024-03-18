#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:16:08 2024

@author: pmchozas
"""
from translation_class import is_sentence_to_translate,extract_quoted_terms,replace_with_quotes,remove_quotes

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 19:51:02 2024

@author: pmchozas
"""

import os
import re
import json
import httpx
import transformers
from transformers import pipeline

#READ FILE

from transformers import MarianMTModel, MarianTokenizer

model_name = f'Helsinki-NLP/opus-mt-en-es'
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)




def model_translation(sentence):
    sentence = sentence.strip()
    # Tokenizar y traducir la oración
    input_ids = tokenizer.encode(sentence, return_tensors="pt")
    translated_ids = model.generate(input_ids, max_length=250, num_beams=3, early_stopping=False)
    translated_sentence = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

    return translated_sentence


def substring_from_last_point(text):
    """
    Returns the substring from the last period ('.') in the input text.

    Args:
    - text (str): The input text.

    Returns:
    - result (str): The substring starting from the last period ('.') in the input text.
    """
    # Find the index of the last period
    last_period_index = text.rfind('.')

    # If a period is found, return the substring starting from the character after the period
    if last_period_index != -1:
        result = text[last_period_index + 1:].strip()
    else:
        # If no period is found, return the entire input text
        result = text

    return result


def error_handler(sentence):
    #print('sent',sentence)
    term= extract_quoted_terms(sentence)[0] # at least 1, and always will be the same
    #print('term',term)
    sentence = remove_quotes(sentence)
    if not sentence[-1] == '.':
        sentence= sentence+'.'
    sentence= sentence +' '+term
    #print('->',sentence)

    translation= model_translation(sentence)
    #print('tr', translation)
    term_translated= substring_from_last_point(translation)
    #print('term', term_translated)
    if term_translated == '':
        #print('again')
        term_translated = model_translation(term)


        translation_new = translation
    else:
        translation_new = translation[:-len(term_translated)]



    output= replace_with_quotes(translation_new, term_translated.lower())

    new_ter= extract_quoted_terms(output)
    if len(new_ter)==0:

        print('>>>>>>>>>>>>>BAD')
        print('Salida', output)
        print('termino',term_translated)



    return output

import ollama


def translate_keyword(key, translated_sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = ""

    for sentence, t_sentence in zip(key.original_annotated_sentences,translated_sentences):


        if not is_sentence_to_translate(sentence):
            translated_text += t_sentence + " "
            continue

        # Agregar punto al final de la oración para tokenización
        #print('vooy')
        translated_sentence= model_translation(sentence)


        ## SE PRODUCE EL FALLO, NO HAY MARCADOR
        if not is_sentence_to_translate(translated_sentence):
            print('bad:',sentence)

            input_ = "Input: \" "+sentence+"\""
            print(ollama.generate(model='translator', prompt=input_)['response'])

            # print(ollama.generate(model='translator', prompt=prompt))

            #translated_sentence= error_handler(sentence)
        # Agregar la oración traducida al texto traducido
        translated_text += translated_sentence + " "
        key.original_annotated_samples.append(sentence)
        key.translated_annotated_samples.append(translated_sentence)

    key.translated_annotated_text = translated_text


    return

def translate_text_original(sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = []
    for sentence in sentences:
        translated_sentence= model_translation(sentence)


        # Agregar la oración traducida al texto traducido
        translated_text.append(translated_sentence)


    return translated_text


import ollama


prompt="""You are a translator of English to Spanish specialized in terms. You will recieve a text in English with a term marked between the XML tag <br> and </br>. Then you translate the text to Spanish. Then yo send again the translated term that was between the XML tag. Some examples:
Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
Output1: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de computación móvil."
Output2: "computación móvil".
Input: "Where have all the <br>PC makers</br> gone?".
Output1: "¿Dónde se han ido todos los fabricantes de PC?".
Output2: "fabricantes de PC?".
Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail".
Output1: "El papel del enredo cuántico del estado inicial se discute en detalle".
Output2: "estado inicial".
Now translate this one:
"""

input_="Input: \"A conferences impact on <br>undergraduate female students</br> in September of 2000, the 3rd Grace Hopper Celebration of Women in Computing was held in Cape Cod, Massachusetts.\""
#print(ollama.generate(model='translator', prompt=prompt))

input_= 'Input: \"A second goal is to describe how this topic fits into the even larger field of MR methods and concepts-in particular, making ties to topics such as wavelets and <br>multigrid methods</br>.\"'

import ollama
response = ollama.chat(model='translator', messages=[
  {
    'role': 'user',
    'content': input_,
  },
])
print(response['message']['content'])

"""
  
    You are a term translator. I give you a sentence with a term marked between the XML <br> and </br>. Give me just the translation into Spanish with the translation of the term marked between the same code. Here are some examples:
    Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
    Output: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de <br>computación móvil</br>."
    Input: "Where have all the <br>PC makers</br> gone?"
    Output: "¿Dónde se han ido todos los <br>fabricantes de PC</br>?"
    Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail"
    Output: "El papel del enredo cuántico del <br>estado inicial</br> se discute en detalle".
    Now translate this one:
    Input: "A conferences impact on <br>undergraduate female students</br> In September of 2000, the 3rd Grace Hopper Celebration of Women in Computing was held in Cape Cod, Massachusetts."

"""

#print(response['message']['content'])

