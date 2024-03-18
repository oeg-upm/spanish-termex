
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers,MAX_COUNTER
#from translation_helsinki import translate_keyword,translate_text_original


#InputPath=   'datasets/Inspec/'
#OutputPath = 'datasets/doc_translations/Helsinki/Inspec/' #'datasets/translation_test/trans'


InputPath=   'datasets/source/SemEval2017/'
OutputPath = 'datasets/doc_translations/Helsinki/SemEval2017/' #'datasets/translation_test/trans'







PathKeys= InputPath+'keys'
PathDocs= InputPath+'docsutf8'

sourcedocs = os.listdir(PathDocs)
targetdocs = os.listdir(OutputPath)

source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs) # for filter


for identifier in source_identifiers:

    if identifier in target_identifiers:
        continue # si está en los ya traducidos pasamos

    try:

        textdoc = read_file_content(PathDocs + '/' + identifier+'.txt')
        textkeys = read_lines(PathKeys + '/' + identifier + '.key')


        # el objeto
        translation = TranslationH(identifier,textdoc, textkeys)

        ## annotation and first translation
        translation.generate_annotated_sentences()

        '''
        translation.translated_text_sentences= translate_text_original(translation.original_text_sentences)

        translation.translated_text = " ".join(translation.translated_text_sentences)

        for key in translation.keys:

            #tr = translate_text_google(annotated, src_lang='en', dest_lang='es')
            tr= translate_keyword(key,translation.translated_text_sentences)
            #translation.translated_annotated_text.append(tr)



        translation.compare_annotated_keywords()
        
        '''
        translation.write_json(OutputPath)
        #print("ERRORS:",translation.error_count)
        break

    except Exception as e:
        print("FATAL ERROR IN "+ str(identifier))
        print(e)
        #break

