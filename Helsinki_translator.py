import transformers
from transformers import pipeline

#READ FILE

import nltk
from transformers import MarianMTModel, MarianTokenizer

nltk.download('punkt')
model_name = f'Helsinki-NLP/opus-mt-en-es'
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)


def translate_text_original(text):


    # Agregar punto al final de la oración para tokenización


        # Tokenizar y traducir la oración
    input_ids = tokenizer.encode(text, return_tensors="pt")
    translated_ids = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    translated_sentence = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    # Agregar la oración traducida al texto traducido


    return translated_sentence