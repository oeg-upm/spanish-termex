from transformers import MarianMTModel, MarianTokenizer, BertTokenizer, BertModel
import torch
def translate_and_detect_terms_with_context(text, terms_to_translate, source_lang, target_lang):
    # Initialize model and tokenizer for English to Spanish translation
    model_name = f'Helsinki-NLP/opus-mt-en-{target_lang}'
    tokenizer_mt = MarianTokenizer.from_pretrained(model_name)
    model_mt = MarianMTModel.from_pretrained(model_name)

    # Translate the text
    translated_text = model_mt.generate(**tokenizer_mt.prepare_seq2seq_batch(text, return_tensors="pt"))
    translated_text = tokenizer_mt.batch_decode(translated_text, skip_special_tokens=True)[0]

    # Initialize model and tokenizer for English BERT
    tokenizer_bert = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model_bert = BertModel.from_pretrained('bert-base-multilingual-cased')

    # Tokenize the translated text
    inputs = tokenizer_bert(text, return_tensors="pt", padding=True, truncation=True)

    # Get the contextual embeddings of the translated text
    outputs = model_bert(**inputs)
    contextual_embeddings = outputs.last_hidden_state

    # Translate the terms and detect their translations
    translated_terms = {}
    for term in terms_to_translate:
        # Translate the term
        translated_term = model_mt.generate(**tokenizer_mt.prepare_seq2seq_batch(term, return_tensors="pt"))
        translated_term = tokenizer_mt.batch_decode(translated_term, skip_special_tokens=True)[0]

        # Tokenize the translated term
        term_inputs = tokenizer_bert(term, return_tensors="pt", padding=True, truncation=True)

        # Get the contextual embeddings of the translated term
        term_outputs = model_bert(**term_inputs)
        term_contextual_embeddings = term_outputs.last_hidden_state

        # Search for the translated term in the translated text using contextual embeddings
        term_found = False
        for i in range(len(contextual_embeddings[0]) - len(term_contextual_embeddings[0])):
            if torch.allclose(contextual_embeddings[0][i:i+len(term_contextual_embeddings[0])], term_contextual_embeddings[0], atol=1e-2):
                term_found = True
                translated_terms[term] = translated_term
                break

    return translated_text, translated_terms

# Example usage
text = "I have a red car and a blue bike."
terms_to_translate = ["red car", "blue bike"]
source_lang = "en"
target_lang = "es"

translated_text, translated_terms = translate_and_detect_terms_with_context(text, terms_to_translate, source_lang, target_lang)
print("Translated text:", translated_text)
print("Translated terms:", translated_terms)

text=  "Bigger is better: the influence of physical size on aesthetic preference judgments The hypothesis that the physical size of an object can influence aesthetic preferences was investigated. In a series of four experiments, participants were presented with pairs of abstract stimuli and asked to indicate which member of each pair they preferred. A preference for larger stimuli was found on the majority of trials using various types of stimuli, stimuli of various sizes, and with both adult and 3-year-old participants. This preference pattern was disrupted only when participants had both stimuli that provided a readily accessible alternative source of preference-evoking information and sufficient attentional resources to make their preference judgments",

term= 'physical size influence'


