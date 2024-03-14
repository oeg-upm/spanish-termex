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
from googletrans import Translator
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
    translated_ids = model.generate(input_ids, max_length=250, num_beams=4, early_stopping=True)
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



    output= replace_with_quotes(translation_new, term_translated)

    new_ter= extract_quoted_terms(output)
    if len(new_ter)==0:
        print('>>>>>>>>>>>>>BAD')
        print('trcute', output)

        print(output)



    return output




def translate_texts(sentences, translated_sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = ""
    for sentence, t_sentence in zip(sentences,translated_sentences):

        if not is_sentence_to_translate(sentence):
            translated_text += t_sentence + " "
            continue

        # Agregar punto al final de la oración para tokenización

        translated_sentence= model_translation(sentence)

        ## SE PRODUCE EL FALLO, NO HAY MARCADOR
        if not is_sentence_to_translate(translated_sentence):
            #print('bad:',translated_sentence)
            translated_sentence= error_handler(sentence)
        # Agregar la oración traducida al texto traducido
        translated_text += translated_sentence + " "



    return translated_text

def translate_text_original(sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = []
    for sentence in sentences:
        translated_sentence= model_translation(sentence)


        # Agregar la oración traducida al texto traducido
        translated_text.append(translated_sentence)


    return translated_text
