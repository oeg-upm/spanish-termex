from transformers import MarianMTModel, MarianTokenizer, BertTokenizer, BertModel
import torch
import ollama
prompt="""You are a translator of English to Spanish specialized in terms and HTML tags. You will recieve a text in English with a term marked between the HTML tag <br> and </br>. In Output1, you generate the full translation of the text. In Output2, you give the translation of the term that was between HTML tags. Some examples:
Input: "The University of Florida, in partnership with Motorola, has held two <br>mobile computing</br> design competitions."
Output1: "La Universidad de Florida, en asociación con Motorola, ha celebrado dos concursos de diseño de computación móvil."
Output2: "computación móvil".
Input: "Where have all the <br>PC makers</br> gone?".
Output1: "¿Dónde se han ido todos los fabricantes de PC?".
Output2: "fabricantes de PC".
Input: "The role of quantum entanglement of the <br>initial state</br> is discussed in detail".
Output1: "El papel del enredo cuántico del estado inicial se discute en detalle".
Output2: "estado inicial".
Input: "A second goal is to describe how this topic fits into the even larger field of MR methods and concepts-in particular, making ties to topics such as wavelets and <br>multigrid methods</br>".
Output1: "Un segundo objetivo es describir cómo este tema se relaciona con el campo más amplio de métodos y conceptos de MR -en particular, estableciendo vínculos con temas como wavelets y métodos multigrid".
Output2: "métodos multigrid"
Now. For this text:
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')


def find_term_position(term, text):
    """
    Encuentra la posición del término en el texto lematizado y recupera el término original.
    Devuelve la posición del término en el texto original y el término original.
    """
    # Tokenizar y lematizar el texto
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Lematizar el término
    term_tokens = word_tokenize(term)
    lemmatized_term = " ".join([lemmatizer.lemmatize(token) for token in term_tokens])

    # Buscar el término lematizado en el texto lematizado
    try:
        start_index = lemmatized_tokens.index(lemmatized_term.split()[0])
        end_index = start_index + len(term_tokens) - 1
        if lemmatized_tokens[start_index:end_index + 1] == lemmatized_term.split():
            original_term = " ".join(tokens[start_index:end_index + 1])
            return start_index, end_index, original_term
        else:
            return -1, -1, None  # Término no encontrado en el texto
    except ValueError:
        return -1, -1, None  # Término no encontrado en el texto


# Ejemplo de uso
term = "lazy dog"
text = "The quick brown fox jumps over the lazy dogs."
start, end, original_term = find_term_position(term, text)
if start != -1:
    print(f"The term '{original_term}' is found starting at position {start} and ending at position {end} in the text.")
else:
    print(f"The term '{term}' is not found in the text.")