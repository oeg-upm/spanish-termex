#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:49:16 2024

@author: pmchozas

"""
import json
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers, separate_sentences, is_sentence_to_translate, extract_quoted_terms, find_last_term_and_remove, translate_text_google, detect_different_translations, check_repetition_percentage
import shutil
import traceback
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

InputPath='datasets/source/SemEval2017/keys/'
InputPath='datasets/source/SemEval2017/docsutf8/'
sourcedocs = os.listdir(InputPath) 
source_identifiers = get_source_identifiers(sourcedocs)


#KEY COUNTER
#SOURCE SemEval2010 3785 keys
#SOURCE SemEval2017 8529 keys
'''
key_counter=0
for identifier in source_identifiers:
    print(identifier)
    file=InputPath+identifier+'.key'
    with open(file, 'r') as f:
        read_key=f.readlines()
        keys=len(read_key)
        key_counter+=keys
        
print(key_counter)
'''

#DOC COUNTER
#SOURCE SemEval2010 2334613
#SOURCE SemEval2017 95877
'''
doc_counter=0
for identifier in source_identifiers:
    print(identifier)
    file=InputPath+identifier+'.txt'
    read_doc=read_file_content(file)
    tokens = nltk.word_tokenize(read_doc)
    doc_counter += len(tokens)
        
print(doc_counter)

'''

InputPath='datasets/source/SemEval2017/keys/'
InputPath='datasets/doc_translations/SemEval2017_GTranslateReviewed/'
sourcedocs = os.listdir(InputPath) 
source_identifiers = get_source_identifiers(sourcedocs)

#DOC TRANSLATION COUNTER
#TRASNLATION SemEval2017 
trans_counter=0
for identifier in source_identifiers:
    source_file= InputPath + '/' + identifier+'.json'
    print(identifier)
    with open(source_file, 'r', encoding='utf-8') as file:
        data=json.load(file)
        text=data['original_translation']
        tokens = nltk.word_tokenize(text)
        trans_counter += len(tokens)

        
print(trans_counter)        

























