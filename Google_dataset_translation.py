
import os
from translation_class import read_lines, read_file_content, Translation, TranslationH,get_source_identifiers, translate_text_google, separate_sentences, is_sentence_to_translate
import json
import shutil
import traceback
#from translation_helsinki import translate_keyword,translate_text_original


#InputPath=   'datasets/Inspec/'
#OutputPath = 'datasets/doc_translations/Helsinki/Inspec/' #'datasets/translation_test/trans'





#InputPath= 'datasets/doc_translations/errors_test'
InputPath=   'datasets/annotated/SemEval2010'
OutputPath = 'datasets/doc_translations/SemEval2010_GTranslate_Annotated' #'datasets/translation_test/trans'

sourcedocs = os.listdir(InputPath)
targetdocs = os.listdir(OutputPath)

source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs) # for filter
fatal_errors= open('datasets/doc_translations/fatal_errors')
error_folder='datasets/doc_translations/errors_semeval'
'''   

for error in fatal_errors:
    new_error=error.rstrip("\n")
    if new_error in target_identifiers:
        
        output_file= OutputPath + '/' + new_error+'.json'
        error_file= error_folder + '/' + new_error+'.json'
        shutil.move(output_file, error_file)
    else: 
        continue
'''
fatal_errors = []

for identifier in source_identifiers:

    if identifier in target_identifiers:
        continue # si está en los ya traducidos pasamos

    try:
        print(identifier)
        translation = Translation()
        
        file_path = InputPath + '/' + identifier+'.json'
        output_file= OutputPath + '/' + identifier+'.json'
        shutil.copy(file_path, output_file)
        with open(file_path, "r") as json_file:
            source_data = json.load(json_file)   
            if 'original_text' in source_data:
                text=source_data['original_text']
                translated_sentences=[]
                sentences=separate_sentences(text)
                for sentence in sentences:
                    tr_sentence=translate_text_google(sentence, src_lang='en', dest_lang='es')
                    translated_sentences.append(tr_sentence)
                translation.original_translation=' '.join(translated_sentences)
                with open(output_file, "r", encoding="utf-8") as out_json_file:
                    output_data = json.load(out_json_file)
                    output_data['original_translation'] = translation.original_translation
                with open(output_file, "w", encoding="utf-8") as out_json_file:
                    json.dump(output_data, out_json_file, ensure_ascii=False, indent=4)
                     
                if 'keys' in source_data:
                    for key in source_data['keys']:
                        translated_br=[]
                        source_br=[]
                        counter=0
                        if 'original_annotated_sentences' in source_data['keys'][key]:
                            print('yes')
                            for sentence in source_data['keys'][key]['original_annotated_sentences']:
                                br=is_sentence_to_translate(sentence)
                                if br==True:
                                    source_br.append(br)
                                    counter+=1
                                    #print("true")
                                    if counter<=10:
                                        replaced_sentence=sentence.replace("<br>", "\"")
                                        replaced_sentence2=replaced_sentence.replace("</br>", "\"")
                                        new_sentence=replaced_sentence2 + " " + key
                                        tr_sentence=translate_text_google(new_sentence, src_lang='en', dest_lang='es')
                                        translated_br.append(tr_sentence)
                                    if counter>=10:
                                        print('COUNTER 10')
                                        break
    
                            # with open(output_file, "r") as out_json_file:
                            #     output_data = json.load(out_json_file)
                            for b in translated_br:
                                output_data['keys'][key]['translated_annotated_samples'].append(b)
                                with open(output_file, 'w', encoding='utf-8') as out_json_file:
                                    json.dump(output_data, out_json_file, ensure_ascii=False, indent=4)
                                    print('--------------FINISH---------------')                
                                  
                                    
                                    

        # el objeto
        #translation = TranslationH(identifier,textdoc, textkeys)

        ## annotation and first translation
        #translation.generate_annotated_sentences()


        # translation.translated_text_sentences= translate_text_original(translation.original_text_sentences)

        # translation.translated_text = " ".join(translation.translated_text_sentences)

        # for key in translation.keys:

        #     #tr = translate_text_google(annotated, src_lang='en', dest_lang='es')
        #     tr= translate_keyword(key,translation.translated_text_sentences)
        #     #translation.translated_annotated_text.append(tr)



        # translation.compare_annotated_keywords()
        
        
        #translation.write_json(OutputPath)
        #print("ERRORS:",translation.error_count)
        #break

    except Exception as e:
        print("FATAL ERROR IN "+ str(identifier))
        fatal_errors.append((identifier))
        print(e)
        print(traceback.format_exc())
        #break
     
      