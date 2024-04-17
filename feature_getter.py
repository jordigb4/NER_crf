import re
import unicodedata
import spacy

class Feature_getter:
    def __init__(self,language = "esp",bigram = True,trigram = True ,morphology= True,lenght = True,prefix = True,lemma = True,POS = True,shape = True):
        
        # Options initailization
        self.morphology = morphology
        self.lenght = lenght
        self.prefix = prefix
        self.lemma = lemma
        self.POS = POS
        self.shape = shape
        self.bigram = bigram
        self.trigram = trigram
        self.last_doc = None #Store the last doc to avoid reprocessing of whole phrase
        self.current_sentence = 0
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
        if idx == 0:
            self.current_sentence += 1
            print("Processing sentence ",self.current_sentence)
            self.last_doc = list(self.nlp(' '.join(tokens)))

        spacy_token_0 = self.last_doc[idx]
        spacy_token_ant = self.last_doc[idx-1] if idx -1 >= 0 else None
        spacy_token_post = self.last_doc[idx+1] if idx +1 < len(tokens) else None

        token_ant = tokens[idx-1] if idx -1 >= 0 else None
        token_post = tokens[idx+1] if idx +1 < len(tokens) else None

        
        feature_list = self.get_feature(token,spacy_token_0,"")

        if self.bigram and spacy_token_ant:
            feature_list.extend(self.get_feature(token_ant,spacy_token_ant,"-1_"))
            if self.trigram and spacy_token_post:
                feature_list.extend(self.get_feature(token_post,spacy_token_post,"+1_"))

        return feature_list
    def get_feature(self,token,spacy_token,position):
        feature_list = []
        # Morphology
        if self.morphology:
            for gender in spacy_token.morph.get("Gender"):
                 feature_list.append(position + "gender_" + gender)
            for number in spacy_token.morph.get("Number"):
                feature_list.append(position +"number_" + number)

        # Length
        if self.lenght:
            feature_list.append(position +"LEN_" + str(len(token)))

        # Prefix
        if self.prefix:
            if len(token) > 0:
                feature_list.append(position +"PRE_" + token[:1])
            if len(token) > 1:
                feature_list.append(position +"PRE_" + token[:2])
            if len(token) > 2:
                feature_list.append(position +"PRE_" + token[:3])
        
        # Lemma
        if self.lemma:
            feature_list.append(position +"LEMMA_" + spacy_token.lemma_)

        # POS
        if self.POS:
            feature_list.append(position +"POS_" + spacy_token.pos_)
        
        # Shape
        if self.shape:
            feature_list.append(position +"SHAPE_" + spacy_token.shape_)
        
        # Capitalization
        if token[0].isupper():
            feature_list.append(position +"CAPITALIZATION")

        # Number
        pattern = r'\d+'
        if re.search(pattern, token) is not None:
            feature_list.append(position +"HAS_NUM")

        # Punctuation
        punc_cat = {"Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po"}
        if all(unicodedata.category(x) in punc_cat for x in token):
            feature_list.append(position +"PUNCTUATION")

        # Suffix up to length 3
        if len(token) > 1:
            feature_list.append(position +"SUF_" + token[-1:])
        if len(token) > 2:
            feature_list.append(position +"SUF_" + token[-2:])
        if len(token) > 3:
            feature_list.append(position +"SUF_" + token[-3:])

        feature_list.append(position +"WORD_" + token)
        return feature_list

