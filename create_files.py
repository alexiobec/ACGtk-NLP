from symtable import Symbol
from nltk.corpus import treebank
import nltk
import re
import create_lex_sign as _lex
import create_tag_sign as _tag
import create_str_sign as _str
import formatting_data as _fmt
from nltk.corpus import brown
from nltk.tag import hmm
from nltk.corpus import genesis


nltk.download('brown')
nltk.download("treebank")
nltk.download("genesis")
tagset = ["ADJ", "ADV", "PRON", "CONJ", "DET", "NOUN", "PONCT", "PRON", "VERB"]

# max_iterations for unsupervised training
max_iter = 2
gen_text = genesis.words("french.txt")
gen_sentences = genesis.sents("french.txt")


def load_pos_unsupervised(num_sents=10000, corpus=brown):
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


def load_pos_supervised(num_sents=10000, corpus=brown):
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


def train(text=brown, num_sents=1000, supervised=True):

    if supervised:
        train_data, tag_list, symbol_list = load_pos_supervised(
            num_sents, corpus=text)
        trainer = hmm.HiddenMarkovModelTrainer(
            states=tag_list, symbols=symbol_list)

        tagger = trainer.train_supervised(train_data)
        return tagger, tag_list, symbol_list

    train_data, symbol_list = load_pos_unsupervised(num_sents, corpus=text)
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


brown_tagger = train(brown, 100000, True)[0]
french_tagger = train(gen_sentences, 100000, False)[0]


create_files_from_scratch("unlabelled_test", "fr",
                          french_tagger, ["Je", "mange", "une", "pomme", "."], typeprob="prob")
