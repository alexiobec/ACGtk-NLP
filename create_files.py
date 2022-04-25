import re
import create_lex_sign as _lex
import create_tag_sign as _tag
import create_str_sign as _str
import formatting_data as _fmt
import nltk
from nltk.corpus import treebank
from nltk.tag import hmm
import numpy as np
from sklearn.model_selection import train_test_split


class Rule:
    def __init__(self, tag_beg, tag_end, probability):
        self.beg = tag_beg
        self.end = tag_end
        self.proba = probability
        self.count = 1


class Word:
    def __init__(self, text, tag, previousWord, proba):
        self.text = text
        self.tag = tag
        self.proba = proba
        self.prev = previousWord


# Train data - pretagged
#train_data = treebank.tagged_sents()[:1000]

def load_pos(num_sents):
    from nltk.corpus import brown

    sentences = brown.tagged_sents(categories="news")[:num_sents]

    tag_re = re.compile(r"[*]|--|[^+*-]+")
    tag_set = set()
    symbols = set()

    cleaned_sentences = []
    for sentence in sentences:
        for i in range(len(sentence)):
            word, tag = sentence[i]
            word = word.lower()  # normalize
            symbols.add(word)  # log this word
            # Clean up the tag.
            tag = tag_re.match(tag).group()
            tag_set.add(tag)
            sentence[i] = (word, tag)  # store cleaned-up tagged token
        cleaned_sentences += [sentence]

    return cleaned_sentences, list(tag_set), list(symbols)


train_data = load_pos(1000)[0]


def create_files_from_scratch(name, language, labelled_text, typeprob="logprob"):
    tag_list, rule_list, word_list = _fmt.get_lists(labelled_text)
    create_files(name, language, tag_list, rule_list,
                 word_list, typeprob=typeprob)
    print("Writing done !")


def create_files(name, language, tag_list, rule_list, word_list, tag=True, str=True, lexic=True, typeprob="logprob"):
    """
    Create the files for the lexicon, the tagger and the string
    :param name: name of the project
    :param language: language of the project
    :param tag_list: list of tags
    :param rule_list: list of rules
    :param word_list: list of words
    :param tag: boolean to create the tagger
    :param str: boolean to create the string
    :param lexic: boolean to create the lexicon
    :param typeprob: type of probability can be "prob" or "logprob" or another string to not show the probabilities
    """
    if lexic:
        _lex.create_lexic(name, language, tag_list,
                          rule_list, word_list)
    if str:
        _str.create_str_sign(name, language, word_list)
    if tag:
        _tag.create_tag_sign(name, language, tag_list,
                             rule_list, word_list, typeprob)


create_files_from_scratch("labelled_test", "en",
                          train_data, typeprob="prob")

# print(_fmt.get_lists(tagged_text,train_tagged_words))
# create_files_from_scratch("test_new","en",tagged_text)
