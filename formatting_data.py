from nltk.corpus import treebank
from nltk.tag import hmm


class Rule:
    def __init__(self, tag_beg, tag_end, probability=1):
        self.beg = tag_beg
        self.end = tag_end
        self.proba = probability


class Word:
    def __init__(self, text, tag, previousWord, proba):
        self.text = text
        self.tag = tag
        self.proba = proba
        self.prev = previousWord


def totallettres(arr):
    total_letters = []
    for word in arr:
        for letter in word.text:
            if letter not in total_letters and letter not in "abcdefghijklmnopqrstuvwxyz":
                total_letters.append(letter)
    return(total_letters)


def clean(str):
    return(str)
    return(str.replace("'", "_APO_").replace('`', "_NAPO_").replace('.', "__DOT_").replace('-', "_HYPHEN_").replace(',', "_COMMA_").replace('1', "_NBR_").replace(':', "_COLON_").replace('(', "_BEGPAR_").replace(')', "_ENDPAR_").replace('2', "_NBR_").replace('9', "_NBR_").replace('3', "_NBR_").replace('7', "_NBR_").replace('4', "_NBR_").replace('6', "_NBR_").replace('8', "_NBR_").replace('$', "_DOLLAR_").replace('0', "_NBR_").replace('5', "_NBR_").replace('&', "_AND_").replace('?', "_INTT_").replace(';', "_SEMCOL_").replace('!', "_EXCL_").replace('/', "_SLASH_"))


def get_lists(supervised_train_data):
    trainer = hmm.HiddenMarkovModelTrainer()
    tagger = trainer.train_supervised(supervised_train_data)
    tag_list = tagger._states
    lexic = tagger._symbols

    # Create rule list
    rule_list = []
    for i, t1 in enumerate(tag_list):
        for j, t2 in enumerate(tag_list):
            prob = -tagger._transitions[t1].logprob(t2)
            if prob != 0.0:
                rule_list.append(Rule(clean(t1), clean(t2), prob))

    # Create word list
    word_list = []
    prev_word = "start"
    for word in lexic:
        for tag in tag_list:
            w = Word(clean(word), clean(tag), prev_word, -
                     tagger._output_logprob(word, tag))
            word_list.append(w)
            prev_word = w
    return([tag_list, rule_list, word_list])
