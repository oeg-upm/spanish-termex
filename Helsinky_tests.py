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
def check_start_with_capital(string):
    if string[0].isupper():
        print("The string starts with a capital letter.")
    else:
        print("The string does not start with a capital letter.")

# Test the function
test_string1 = "9Hello"
test_string2 = "[world"

check_start_with_capital(test_string1)
check_start_with_capital(test_string2)