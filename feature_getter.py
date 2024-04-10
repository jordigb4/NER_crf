import re
import unicodedata
import spacy
class Feature_getter:
    def __init__(self,language = "esp", morphology= True,lenght = True,prefix = True,lemma = True,POS = True,shape = True):
        
        # Options initailization
        self.morphology = morphology
        self.lenght = lenght
        self.prefix = prefix
        self.lemma = lemma
        self.POS = POS
        self.shape = shape

        # Features cache
        self.token_cache = {}

        #Model loading
        if language == "esp":
            self.nlp = spacy.load("es_core_news_sm")
        elif language == "ned":
            self.nlp = spacy.load("nl_core_news_sm")
        else:
            raise Exception("Language not in the scope of the model") 


    
    def __call__(self, tokens, idx):
        """
        Extract basic features about this word including
            - Current word
            - is it capitalized?
            - Does it have punctuation?
            - Does it have a number?
            - Suffixes up to length 3

        Note that : we might include feature over previous word, next word etc.

        :return: a list which contains the features
        :rtype: list(str)
        """
        token = tokens[idx]


        feature_list = []

        if not token:
            return feature_list

        # SpAcy NLP on tokens if not done already
        if token not in self.token_cache:
            
            for element in tokens:
                
                self.token_cache[element.text] = {
                    "gender": element.morph.get("Gender"),
                    "number": element.morph.get("Number"),
                    "lemma": element.lemma_,
                    "pos_tag": element.pos_,
                    "shape": element.shape_
                }

        # Morphology
        if self.morphology:
            feature_list.append(str(self.token_cache[token]["gender"]))
            feature_list.append(str(self.token_cache[token]["number"]))

        # Length
        if self.lenght:
            feature_list.append("LEN_" + str(len(token)))

        # Prefix
        if self.prefix:
            if len(token) > 0:
                feature_list.append("PRE_" + token[:1])
            if len(token) > 1:
                feature_list.append("PRE_" + token[:2])
            if len(token) > 2:
                feature_list.append("PRE_" + token[:3])
        
        # Lemma
        if self.lemma:
            feature_list.append("LEMMA_" + self.token_cache[token]["lemma"])

        # POS
        if self.POS:
            feature_list.append("POS_" + self.token_cache[token]["pos_tag"])
        
        # Shape
        if self.shape:
            feature_list.append("SHAPE_" + self.token_cache[token]["shape"])
        
        # Capitalization
        if token[0].isupper():
            feature_list.append("CAPITALIZATION")

        # Number
        pattern = r'\d+'
        if re.search(pattern, token) is not None:
            feature_list.append("HAS_NUM")

        # Punctuation
        punc_cat = {"Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"}
        if all(unicodedata.category(x) in punc_cat for x in token):
            feature_list.append("PUNCTUATION")

        # Suffix up to length 3
        if len(token) > 1:
            feature_list.append("SUF_" + token[-1:])
        if len(token) > 2:
            feature_list.append("SUF_" + token[-2:])
        if len(token) > 3:
            feature_list.append("SUF_" + token[-3:])

        feature_list.append("WORD_" + token)
        return feature_list

