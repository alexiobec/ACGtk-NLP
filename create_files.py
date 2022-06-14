import create_lex_sign as _lex
import create_tag_sign as _tag
import create_str_sign as _str
import formatting_data as _fmt
import nltk
import re
from nltk.tag import hmm
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.corpus import genesis
nltk.download('brown')
nltk.download("genesis")
nltk.download('treebank')

# tagset to use for unsupervised training
tagset = ["ADJ", "ADV", "PRON", "CONJ", "DET", "NOUN", "PONCT", "PRON", "VERB"]


def load_pos_unsupervised(corpus, num_sents=10000):
    """
    :param num_sents: number of sentences to load
    :param corpus: corpus to load from
    :return: list of sentences
    """
    sentences = corpus[:num_sents]

    symbols = set()

    cleaned_sentences = []
    for sentence in sentences:
        for i in range(len(sentence)):
            word = sentence[i]
            word = word.lower()  # normalize
            symbols.add(word)  # log this word
            sentence[i] = (word, '')  # store cleaned-up non-tagged token
        cleaned_sentences += [sentence]

    return cleaned_sentences, list(symbols)


def load_pos_supervised(corpus, num_sents=10000):
    """
    :param num_sents: number of sentences to load
    :param corpus: corpus to load from
    :return: list of sentences, list of tags, list of symbols
    """
    sentences = corpus.tagged_sents()[:num_sents]

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


def train(text, num_sents=10000, supervised=True, max_iter=20):

    if supervised:
        train_data, tag_list, symbol_list = load_pos_supervised(
            text, num_sents)
        trainer = hmm.HiddenMarkovModelTrainer(
            states=tag_list, symbols=symbol_list)

        tagger = trainer.train_supervised(train_data)
        return tagger, tag_list, symbol_list
    else:
        train_data, symbol_list = load_pos_unsupervised(text, num_sents)
        trainer = hmm.HiddenMarkovModelTrainer(
            states=tagset, symbols=symbol_list)
        tagger = trainer.train_unsupervised(text, max_iterations=max_iter)
        return tagger, symbol_list


def create_files_from_scratch(name, language, tagger, text, typeprob="logprob"):
    """
    Create the files for the lexicon, the tagger and the string from a labelled text
    """
    tag_list, rule_list, word_list = _fmt.get_lists(tagger, text)
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
        _lex.create_lexic(name, language,
                          rule_list, word_list)
    if str:
        _str.create_str_sign(name, language, word_list)
    if tag:
        _tag.create_tag_sign(name, language, tag_list,
                             rule_list, word_list, typeprob)
