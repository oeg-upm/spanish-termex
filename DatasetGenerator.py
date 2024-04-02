import os
from translation_class import read_lines, read_file_content, Translation, TranslationH, get_source_identifiers

# from translation_helsinki import translate_keyword,translate_text_original
import json


def order_list(original_list, reference_list):
    ordered_list = []

    # Iterate through the reference list and add elements to the ordered list
    for item in reference_list:
        if item in original_list:
            ordered_list.append(item)
            # Remove the item from the original list to avoid duplicates
            original_list.remove(item)

    # Append any remaining elements from the original list to the ordered list
    ordered_list.extend(original_list)

    return ordered_list

class GenericTranslation():
    def __init__(self, jsonfile,referencelist):
        with open(jsonfile, 'r') as file:
            # Load the JSON data into a Python dictionary
            data = json.load(file)

        #self.id = data['id']
        self.original_text = data['original_text']
        self.translated_text = data['original_translation']

        self.error_count = data['error_count']
        keys = data['keys']
        self.keys_original=[]
        self.keys_trans= []
        if referencelist == None:

            for key in keys.keys():
                self.keys_original.append(key)
                self.keys_trans.append(keys[key]['translated_key'])
        else:
            prov_list=[]
            for key in keys.keys():
                prov_list.append(key)
            self.keys_original= order_list(prov_list,referencelist)
            for key in self.keys_original:
                self.keys_trans.append(keys[key]['translated_key'])




def write_text(nombre_archivo, contenido):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)

def write_keys(nombre_archivo, lineas):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        for linea in lineas:
            archivo.write(linea + '\n')







InputPath1=   'datasets/source/SemEval2017/'
InputPath2=   'datasets/doc_translations/OpenAI/SemEval2017_2ReviewedComplete/'
OutputPath = 'datasets/target/SemEval2017_GPT3/' #'datasets/translation_test/trans'



PathKeys = InputPath1 + 'keys'
PathDocs = InputPath1 + 'docsutf8'

sourcedocs = os.listdir(InputPath2)
targetdocs = os.listdir(OutputPath)

source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs)  # for filter





for identifier in source_identifiers:

    if identifier in target_identifiers:
        continue  # si está en los ya traducidos pasamos

    try:

        textkeys = read_lines(PathKeys + '/' + identifier + '.key')

        #print(textkeys)
        #in semeval2017 textkeys puede ser none
        #textkeys=None

        trans= GenericTranslation(InputPath2+str(identifier)+'.json',None)

        PathKeys2 = OutputPath + 'keys/'+str(identifier)+'.key'
        PathDocs2 = OutputPath + 'docsutf8/'+str(identifier)+'.txt'

        write_keys(PathKeys2,trans.keys_trans)
        write_text(PathDocs2,trans.translated_text)





        # print("ERRORS:",translation.error_count)


    except Exception as e:
        print("FATAL ERROR IN " + str(identifier))
        print(e)
        # break

