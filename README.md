# spanish-termex
State of the art of automatic term extraction and keyword extraction for English and Spanish languages.
This repository contains the scripts for the translation of SemEval2010 and 2017 datasets for keyword extraction into Spanish language.
Also, the evaluation process with the main soa AKE methods implemented by the library PKE is developed.


## Installation
On Python 3.9

Libraries and versions on file Requirements.txt


Also remember the spacy model for Spanish

´´´
python -m spacy download es_core_news_sm

´´´

## Structure of the repo

The main folder with results is 'datasets'. Inside the directory:

- Source: Original datasets
- Target: Final translated datasets 
- doc_translation: Intermediate results, obtained by different translators. 



