import re
import unicodedata
import spacy

class Feature_getter_be:

    def __init__(self):
        pass
        

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

        # Capitalization
        if token[0].isupper():
            feature_list.append("CAPITALIZATION")

        # Number
        pattern = re.compile(r"\d")
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
        with open("spacy_tokens_be.txt", "a") as f:
            f.write(f"{feature_list}\n")
        return feature_list