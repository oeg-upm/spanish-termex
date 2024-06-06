
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers
#from translation_helsinki import translate_keyword,translate_text_original
import openaiwe

#InputPath=   'datasets/Inspec/'
#OutputPath = 'datasets/doc_translations/Helsinki/Inspec/' #'datasets/translation_test/trans'


InputPath=   'datasets/annotated/SemEval2017/'
OutputPath = 'datasets/doc_translations/OpenAI/SemEval2017_2/'

InputPath=   'datasets/annotated/SemEval2010/'
OutputPath = 'datasets/doc_translations/OpenAI/SemEval2010/'

import time




sourcedocs = os.listdir(InputPath)
targetdocs = os.listdir(OutputPath)

source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs) # for filter

counter=0
start = time.time()


for identifier in source_identifiers:

    if identifier in target_identifiers:
        continue # si está en los ya traducidos pasamos

    try:
        print(identifier)
        continue
        translation= TranslationH(identifier,'','')
        file_stats = os.stat(InputPath+str(identifier)+'.json')

        print(file_stats)
        print(f'File Size in Bytes is {file_stats.st_size}')
        translation.construct_from_json(InputPath+str(identifier)+'.json')


        translation.translated_text_sentences= openaiwe.translate_text_original2(translation.original_text_sentences)

        translation.translated_text = " ".join(translation.translated_text_sentences)
        print('translated')

        for key in translation.keys:
            #print(key.original_annotated_sentences)
            print('key ',key)
            openaiwe.translate_keyword(key,translation.translated_text_sentences)

        translation.compare_annotated_keywords()
        

        translation.write_json(OutputPath)
        #print("ERRORS:",translation.error_count)
        #break
        if counter==1:
            break
        #counter=counter+1

    except Exception as e:
        print("FATAL ERROR IN "+ str(identifier))
        print(e)
        #break


end = time.time()
print(end - start)