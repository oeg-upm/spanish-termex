

import pke
import yake
from multi_rake import Rake


def clean_pkeresutls(res):
    newLis=[]
    for r in res:
        newLis.append(r[0].lower())
    return newLis

class RakeExtractor():
    def __init__(self):
        """rake = Rake(
    min_chars=3,
    max_words=3,
    min_freq=1,
    language_code=None,  # 'en'
    stopwords=None,  # {'and', 'of'}
    lang_detect_threshold=50,
    max_words_unknown_lang=2,
    generated_stopwords_percentile=80,
    generated_stopwords_max_len=3,
    generated_stopwords_min_freq=2,
)"""
        self.extractor = Rake(min_chars=3,language_code='es')

    def extract_best(self,text, n):
        keywords = self.extractor.apply(
            text,

        )
        return clean_pkeresutls(keywords[:n])


class TopicRankExtractor():
    def __init__(self):
        # initialize keyphrase extraction model, here TopicRank
        self.extractor = pke.unsupervised.TopicRank()

    def extract_best(self,text, n):
        # load the content of the document, here document is expected to be a simple
        # test string and preprocessing is carried out using spacy
        self.extractor.load_document(input=text, language='es')

        # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
        # and adjectives (i.e. `(Noun|Adj)*`)
        self.extractor.candidate_selection()

        # candidate weighting, in the case of TopicRank: using a random walk algorithm
        self.extractor.candidate_weighting()

        # N-best selection, keyphrases contains the 10 highest scored candidates as
        # (keyphrase, score) tuples
        keyphrases = self.extractor.get_n_best(n)
        return clean_pkeresutls(keyphrases)



class YakeExtractor():
    def __init__(self):
        self.extractor = yake.KeywordExtractor(lan="es")

    def extract_n_best(self,text,n):
        keywords = self.extractor.extract_keywords(text)
        
        #return clean_pkeresutls(keywords[:n])
        return keywords




class TextRankExtractor():
    def __init__(self):
        # initialize keyphrase extraction model, here TopicRank
        self.extractor = pke.unsupervised.TextRank()

    def extract_best(self,text, n):
        # load the content of the document, here document is expected to be a simple
        # test string and preprocessing is carried out using spacy
        self.extractor.load_document(input=text, language='es')

        # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
        # and adjectives (i.e. `(Noun|Adj)*`)
        self.extractor.candidate_selection()

        # candidate weighting, in the case of TopicRank: using a random walk algorithm
        self.extractor.candidate_weighting()

        # N-best selection, keyphrases contains the 10 highest scored candidates as
        # (keyphrase, score) tuples
        keyphrases = self.extractor.get_n_best(n)
        return clean_pkeresutls(keyphrases)

class SingleRankExtractor():
    def __init__(self):
        # initialize keyphrase extraction model, here TopicRank
        self.extractor = pke.unsupervised.SingleRank()

    def extract_best(self,text, n):
        # load the content of the document, here document is expected to be a simple
        # test string and preprocessing is carried out using spacy
        self.extractor.load_document(input=text, language='es')

        # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
        # and adjectives (i.e. `(Noun|Adj)*`)
        self.extractor.candidate_selection()

        # candidate weighting, in the case of TopicRank: using a random walk algorithm
        self.extractor.candidate_weighting()

        # N-best selection, keyphrases contains the 10 highest scored candidates as
        # (keyphrase, score) tuples
        keyphrases = self.extractor.get_n_best(n)
        return clean_pkeresutls(keyphrases)


'''
TextRank (Mihalcea and Tarau, 2004)
SingleRank (Wan and Xiao, 2008)
TopicRank (Bougouin et al., 2013)
TopicalPageRank (Sterckx et al., 2015)
PositionRank (Florescu and Caragea, 2017)
MultipartiteRank (Boudin, 2018)
'''
