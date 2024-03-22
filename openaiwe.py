
import os
from openai import OpenAI
from translation_class import replace_with_quotes_h, replace_with_quotes_hard


def is_sentence_to_translate(sentence):
  # if re.search(r'\uFFFC', sentence):
  if '<br>' in sentence:
    return True
  return False

client = OpenAI(
    # This is the default and can be omitted
  api_key=""
)

prompt1= """
You are a translator of English to Spanish. You will recieve a text in English, sometimes with a term marked between the XML tag <br> and </br>. Then you translate the text to Spanish maintaining the XML tags <br> and </br> between the term. Some examples:
Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
Output: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de <br>computación móvil</br>."
Input: "Where have all the <br>PC makers</br> gone?".
Output: "¿Dónde se han ido todos los <br>fabricantes de PC</br>?".
Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail".
Output: "El papel del enredo cuántico del <br>estado inicial</br> se discute en detalle".
Input: "It often exploits an <br>optical diffusion model-based image reconstruction algorithm</br> to estimate spatial property values from measurements of the light flux at the surface of the tissue."
Output: "A menudo se utiliza un <br>algoritmo de reconstrucción de imágenes basado en un modelo de difusión óptica</br> para estimar los valores de propiedades espaciales a partir de medidas de la flujo de luz en la superficie del tejido."
"""

prompt2= "You are a scientific translator of English to Spanish. Translate the following sentence to Spanish."
prompt25= ("You are a scientific translator of English to Spanish language. Translate the text to Spanish. "
           "The text has each sentence in a line. Keep the original line breaks.")



def translate_keyword(key, translated_sentences):

    if not key.is_in_text: ## no está anotada, por lo tanto no pertenece al texto
        translated_term= gpt_translator(key.key).strip()
        key.translated_term= translated_term
        return

    # Traducir cada frase y reconstruir el texto traducido
    translated_text = ""
    counter=0
    for sentence, t_sentence in zip(key.original_annotated_sentences ,translated_sentences):

        if not is_sentence_to_translate(sentence):
            translated_text += t_sentence + " "
            continue

        # Agregar punto al final de la oración para tokenización

        #translated_sentence= gpt_translator_key(sentence) #old version
        translated_term= gpt_translator_key2(sentence,t_sentence)
        translated_sentence = replace_with_quotes_hard(t_sentence, translated_term.strip())
        val = is_sentence_to_translate(translated_sentence)

        '''
        if not val:
            print("error")
            print(translated_term,translated_sentence)
            print(key, sentence)
        '''



        # Agregar la oración traducida al texto traducido
        translated_text += translated_sentence + " "
        key.original_annotated_samples.append(sentence)
        key.translated_annotated_samples.append(translated_sentence)

        if counter == 4:
            break
        counter = counter + 1

    key.translated_annotated_text = translated_text


    return

def translate_text_original(sentences):


    # Traducir cada frase y reconstruir el texto traducido
    text_= ''
    for sentence in sentences:
        text_ = text_+ sentence +'\n'
    translated_sentence = gpt_translator(text_)
    translated_text = translated_sentence.split('\n')
    if len(sentences)!= len(translated_text):
        print(">>>> Fatal error in segmentation")
    return translated_text

def translate_text_original2(sentences):


    # Traducir cada frase y reconstruir el texto traducido
    translated_text = []
    for sentence in sentences:
        translated_sentence= gpt_translator(sentence)
        # Agregar la oración traducida al texto traducido
        translated_text.append(translated_sentence)


    return translated_text




def gpt_translator(text):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
      {"role": "system", "content": prompt2},
      {"role": "user",
       "content": text}
    ]
    )
    return completion.choices[0].message.content


def gpt_translator_key(text):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      temperature=0,
      messages=[
        {"role": "system", "content": prompt1},
        {"role": "user", "content": "Input: \" " +text +"\""}
      ]
    )
    return completion.choices[0].message.content.replace("\"" ,"")



prompt3= """
You are a scientific translator of English to Spanish specialized in terminology. 
I give you one sentence in English and the same sentence translated to Spanish. 
The English sentence has a term between the marks <br> and </br>. 
Identify in the Spanish sentence which words correspond to the same original term.
The output term is in Spanish. 
Some examples
English sentence: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions".
Spanish sentence : "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de computación móvil".
Output: computación móvil
English sentence: "There, we assume that <br>coefficients of non-renormalizable terms</br> are suppressed enough to be neglected".
Spanish sentence: "Aquí, asumimos que los coeficientes de los términos no renormalizables están suficientemente suprimidos como para ser ignorados".
Output:  coeficientes de los términos no renormalizables
English sentence: "It often exploits an <br>optical diffusion model-based image reconstruction algorithm</br> to estimate spatial property values from measurements of the light flux at the surface of the tissue."
Spanish sentence: "A menudo se utiliza un algoritmo de reconstrucción de imágenes basado en un modelo de difusión óptica para estimar los valores de propiedades espaciales a partir de medidas de la flujo de luz en la superficie del tejido."
Output: algoritmo de reconstrucción de imágenes basado en un modelo de difusión óptica
English: "A second group of experiments is aimed at extensions of the baseline methods that exploit characteristic features of the UvT Expert Collection; specifically, we propose and evaluate refined expert finding and profiling methods that incorporate <br>topicality and organizational structure</br>."
Spanish: "Un segundo grupo de experimentos está dirigido a extensiones de los métodos base que aprovechan las características distintivas de la Colección de Expertos de UvT; específicamente, proponemos y evaluamos métodos refinados de búsqueda y perfilado de expertos que incorporan la topicalidad y la estructura organizativa."
output: topicalidad y la estructura organizativa
"""

"""
"Where have all the <br>PC makers</br> gone?".
Spanish sentence: "¿Dónde se han ido todos los fabricantes de PC?".
Output: fabricantes de PC
"""
def gpt_translator_key2(text1,text2):
    completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          temperature=0,
          messages=[
            {"role": "system", "content": prompt3},
            {"role": "user", "content": "English: \"" +text1 +"\"\nSpanish: \""+text2+"\"\nOutput: "}
          ]
        )
    res= completion.choices[0].message.content.strip()
    #print(completion)
    return res
#res= translate_text_original(["Hello, world this is a test to follow instructions"])
#print(res)

import re
def replace_with_quotes_hard_gpt(text, term):
    escaped_substring = re.escape(term)
    # Construct the regex pattern to find the substring
    pattern = re.compile('(' + escaped_substring + ')',re.IGNORECASE)
    newterm = "<br>" + term + "</br>"  # f'"{term}"'
    # Use re.sub() to replace the matched substring with annotated version
    replaced_text = re.sub(pattern, newterm, text,re.IGNORECASE)

    return replaced_text




""" TEST PROMTS

text1= "A second group of experiments is aimed at extensions of the baseline methods that exploit characteristic features of the UvT Expert Collection; specifically, we propose and evaluate refined expert finding and profiling methods that incorporate <br>topicality and organizational structure</br>."
text2="Un segundo grupo de experimentos está dirigido a extensiones de los métodos base que aprovechan las características distintivas de la Colección de Expertos de UvT; específicamente, proponemos y evaluamos métodos refinados de búsqueda y perfilado de expertos que incorporan la topicalidad y la estructura organizativa."

text1 ="<br>broad expertise retrieval</br> in Sparse Data Environments Krisztian Balog ISLA, University of Amsterdam Kruislaan 403, 1098 SJ Amsterdam, The Netherlands kbalog@science.uva.nl Toine Bogers ILK, Tilburg University P.O."
text2 = "Recuperación de amplia experiencia en entornos de datos dispersos Krisztian Balog ISLA, Universidad de Ámsterdam Kruislaan 403, 1098 SJ Ámsterdam, Países Bajos kbalog@science.uva.nl Toine Bogers ILK, Universidad de Tilburg P.O."

res= gpt_translator_key2(text1,text2)
print(res)



translated_sentence = replace_with_quotes_hard_gpt(text2, res.strip())
val = is_sentence_to_translate(translated_sentence)
print(val)
print(translated_sentence)
"""