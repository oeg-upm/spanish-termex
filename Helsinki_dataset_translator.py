
import os
from translation_class import read_lines,read_file_content,Translation,translate_text_google
from translation_helsinki import translate_text

def get_source_identifiers(file_list):
    identifiers=[]
    for file_ in file_list:
        if file_.endswith('.txt'):
            identifiers.append(file_.replace('.txt',''))
        if file_.endswith('.json'):
            identifiers.append(file_.replace('.json',''))

    return identifiers



'''
ONLY INPUT
'''


InputPath=   'datasets/translation_test/'
OutputPath = 'datasets/translation_test/trans'#'datasets/doc_translations/Helsinki/Inspec/'


'''
REST
'''

PathKeys= InputPath+'keys'
PathDocs= InputPath+'docsutf8'

sourcedocs = os.listdir(PathDocs)
targetdocs = os.listdir(OutputPath)

source_identifiers = get_source_identifiers(sourcedocs)
target_identifiers = get_source_identifiers(targetdocs) # for filter

print(source_identifiers)
print(target_identifiers)


for identifier in source_identifiers:

    if identifier in target_identifiers:
        continue # si está en los ya traducidos pasamos

    textdoc = read_file_content(PathDocs + '/' + identifier+'.txt')
    textkeys = read_lines(PathKeys + '/' + identifier + '.key')


    # el objeto
    translation = Translation(textdoc, textkeys)

    translation.id = identifier


    list_annotations = translation.generate_annotated_sentences()
    '''HELSINKI
    translation.original_translation = translate_text_google(textdoc, src_lang='en', dest_lang='es')
    for annotated in list_annotations:
        tr = translate_text_google(annotated, src_lang='en', dest_lang='es')
        print(tr)
        translation.translated_annotated_text.append(tr)
    '''
    translation.original_translation = translate_text(textdoc)
    for annotated in list_annotations:
        tr = translate_text(annotated)
        translation.translated_annotated_text.append(tr)

    translation.compare_annotated_keywords()
    translation.write_json(OutputPath)


