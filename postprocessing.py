#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 14:55:27 2024

@author: pmchozas
"""

import json
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers, separate_sentences, is_sentence_to_translate, extract_quoted_terms, find_last_term_and_remove, translate_text_google, detect_different_translations
import shutil
import traceback

SourcePath = 'datasets/doc_translations/SemEval2010_GTranslate_Annotated' 
OutPath='datasets/doc_translations/postprocessed2010' 
sourcedocs = os.listdir(SourcePath) 
targetdocs= os.listdir(OutPath)
source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs)





translation = Translation()
fatal_errors = []
for identifier in source_identifiers:
    if identifier in target_identifiers:
        continue # si está en los ya traducidos pasamos
    try:
        print(identifier)
        source_file= SourcePath + '/' + identifier+'.json'
        output_file= OutPath + '/' + identifier+'.json'
        shutil.copy(source_file, output_file)
        with open(source_file, 'r', encoding='utf-8') as file:
            data=json.load(file)
            for key in data['keys']:
                print(key)
                translated_terms=[]
                modified_translated_sentences=[]
                if 'translated_annotated_samples' in data['keys'][key] and data['keys'][key]['translated_annotated_samples'] is not None and data['keys'][key]['translated_annotated_samples'] !=[] :
                    for translated in data['keys'][key]['translated_annotated_samples']:
                        res=find_last_term_and_remove(translated)
                        print(res)
                        term=res[0]
                        modified_translated_sentences.append(res[1])
    
                        print('esto es term')
                        print(term)
                        if term != None:
                            translated_terms.append(term.strip())
                        terms=extract_quoted_terms(translated)
                        for t in terms:
                            translated_terms.append(t)
                    print('Todas las candidates')
                    print(translated_terms)
                    if detect_different_translations(translated_terms): 
                        translated_key=translated_terms[0]
                        print('esto es translated key '+ translated_key)
                    else:
                        translated_key=""
                        
                    with open(output_file, "r", encoding="utf-8") as out_json_file:
                        output_data = json.load(out_json_file)
                        output_data['keys'][key]['translated_key']=translated_key
                        output_data['keys'][key]['candidates']=translated_terms
                        output_data['keys'][key]['translated_annotated_samples']=modified_translated_sentences
                        
                    with open(output_file, "w", encoding="utf-8") as out_json_file:
                        json.dump(output_data, out_json_file, ensure_ascii=False, indent=4)
                else:
                    print(key + ' ----  NO CANDIDATES, esto es translated keyword sin contexto')
                    trans_key=translate_text_google(key, src_lang='en', dest_lang='es')
                    print(trans_key)
                    
                    with open(output_file, "r", encoding="utf-8") as out_json_file:
                        output_data = json.load(out_json_file)
                        output_data['keys'][key]['translated_key']=trans_key
    
                        
                    with open(output_file, "w", encoding="utf-8") as out_json_file:
                        json.dump(output_data, out_json_file, ensure_ascii=False, indent=4)

                
    except Exception as e:
        print("FATAL ERROR IN "+ str(identifier))
        fatal_errors.append((identifier))
        print(e)
        print(traceback.format_exc())