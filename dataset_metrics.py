#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:49:16 2024

@author: pmchozas

"""
import json
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers, separate_sentences, is_sentence_to_translate, extract_quoted_terms, find_last_term_and_remove, detect_different_translations, check_repetition_percentage
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
InputPath='datasets/doc_translations/SemEval2017_GTranslate/'
RevPath= 'datasets/doc_translations/SemEval2017_GTranslateReviewed/'
RevPath= 'datasets/doc_translations/SemEval2010_GTranslateReviewed/'
sourcedocs = os.listdir(InputPath) 
revdocs=os.listdir(RevPath)
source_identifiers = get_source_identifiers(sourcedocs)
rev_identifiers = get_source_identifiers(revdocs)

#TRANSLATION COUNTER GOOGLE TRANSLATE (hay un desfase, a ver qué pasa)
#TRANSLATION SemEval2017 104606
#TRANSLATION SemEval2010 2501394
#Translated key SemEval2010 3762
#Translated key SemEval2017 8525

'''
transkey_counter=0
for identifier in rev_identifiers:
    rev_file= RevPath + '/' + identifier+'.json'
    with open(rev_file, 'r', encoding='utf-8') as file:
        data=json.load(file)
        for key in data['keys']:
            if data['keys'][key]['translated_key']==" ":
                #transkey_counter+=1
                print(identifier + ' ' + key)
                            
        #tokens = nltk.word_tokenize(text)
        #trans_counter += len(tokens)
print(transkey_counter)          
'''


InputPath='datasets/doc_translations/SemEval2017_GTranslate/'
# RevPath= 'datasets/doc_translations/SemEval2017_GTranslateReviewed/'
# RevPath= 'datasets/doc_translations/SemEval2010_GTranslateReviewed/'
sourcedocs = os.listdir(InputPath) 
# revdocs=os.listdir(RevPath)
source_identifiers = get_source_identifiers(sourcedocs)
# rev_identifiers = get_source_identifiers(revdocs)


#ERROR COUNTER GOOGLE TRANSLATE
#SemEval2010 1553
#SemEval2017 503
'''
error_counter=0
for identifier in source_identifiers:
    file= InputPath + '/' + identifier+'.json'
    with open(file, 'r', encoding='utf-8') as file:
        data=json.load(file)
        error_num=data['error_count']
        if error_num > 0: 
           error_counter+= error_num
        # for key in data['keys']:
        #     if data['keys'][key]['translated_key']=="":
        #         error_counter+=1

print(error_counter)
'''



InputPath='datasets/source/SemEval2010/keys/'
TrPath='datasets/doc_translations/SemEval2010_GTranslateReviewed/'
sourcedocs = os.listdir(InputPath) 
trdocs= os.listdir(TrPath)
source_identifiers = get_source_identifiers(sourcedocs)
tr_identifiers= get_source_identifiers(trdocs)


#DESFASES ENTRE SOURCE Y TR


for identifier in source_identifiers:
    #print(identifier)
    sr_file=InputPath+identifier+'.key'
    with open(sr_file, 'r') as f:
        read_key=f.readlines()
        sr_key_counter=len(read_key)
    
    if identifier in tr_identifiers:
        tr_key_counter=0
        tr_file=TrPath+identifier+'.json'
        with open(tr_file, 'r', encoding='utf-8') as file:
            data=json.load(file)
            for key in data['keys']:
                tr_key_counter+=1
        if sr_key_counter != tr_key_counter:
            print('DESFASE: '+identifier + ' SR=' + str(sr_key_counter) + ' TR=' + str(tr_key_counter))
    
                














































