# Benchmark for Automatic Keyword Extraction in Spanish: Datasets and Methods
Tasks such as document indexing or information retrieval still seem to heavily rely on keywords, even in the LLMs era. However, there is still a need for automatic keyword extraction works and training sets in languages other than English. To the best of our knowledge, no datasets for keyword extraction in Spanish are publicly available for training or evaluation purposes. Additionally, those innovative keyword extraction methods that rely on language models are not being adapted to language models in other languages. To palliate this situation, this work proposes a method to translate into Spanish two of the main gold standard datasets used by community, while preserving semantics and terms. Then, the main state-of-the-art methods are evaluated against the new translated datasets. The methods used for the evaluation have been configured or re-implemented for Spanish. 

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



## Acknowledgments 
Para su desarrollo este código ha recibido financiación del proyecto INESData (Infraestructura para la INvestigación de ESpacios de DAtos distribuidos en UPM), un proyecto financiado en el contexto de la convocatoria UNICO I+D CLOUD del Ministerio para la Transformación Digital y de la Función Pública en el marco del PRTR financiado por Unión Europea (NextGenerationEU).


## Paper Citation

```bibtext
@inproceedings{Calleja2024,
  author    = {Pablo Calleja and Patricia Martín-Chozas and Elena Montiel-Ponsoda},
  title     = {Benchmark for Automatic Keyword Extraction in Spanish: Datasets and Methods},
  booktitle = {Poster Proceedings of the 40th Annual Conference of the Spanish Association for Natural Language Processing 2024 (SEPLN-P 2024)},
  series    = {CEUR Workshop Proceedings},
  volume    = {3846},
  pages     = {132--141},
  year      = {2024},
  publisher = {CEUR-WS.org},
  address   = {Valladolid, Spain},
  month     = {September 24-27},
  urn       = {urn:nbn:de:0074-3846-7},
  url       = {https://ceur-ws.org/Vol-3846/}
}
```
