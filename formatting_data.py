class Rule:
    def __init__(self, tag_beg, tag_end, probability, logproba):
        self.beg = tag_beg
        self.end = tag_end
        self.proba = probability
        self.logproba = logproba


class Word:
    def __init__(self, text, tag, previousWord, proba, logproba):
        self.text = text
        self.tag = tag
        self.proba = proba
        self.prev = previousWord
        self.logproba = logproba


def totalletters(arr):
    """
    :param arr: list of words
    :return: a list of the characters in arr that aren't in the alphabet
    """
    total_letters = []
    for word in arr:
        for letter in word.text:
            if letter not in total_letters and letter not in "abcdefghijklmnopqrstuvwxyz":
                total_letters.append(letter)
    return(total_letters)


def clean(word):
    """
    :param word: string
    :return: string where all non-alphabetic characters are replaced with a name of the form _X_
    """
    i = 0
    while i < len(word):
        if word[i].isdigit():
            beg = i
            end = i
            while end < len(word) and (word[end].isdigit() or word[end] in {",", ".", "-"}):
                end += 1
            word = f"{word[:beg]}_NBR_{word[end:]}"
        i += 1
    return word.replace("'", "_APO_").replace('`', "_NAPO_").replace('.', "__DOT_").replace('-', "_HYPHEN_")\
        .replace(',', "_COMMA_").replace(':', "_COLON_").replace('(', "_BEGPAR_").replace(')', "_ENDPAR_")\
        .replace('$', "_DOLLAR_").replace('&', "_AND_").replace('?', "_INTT_").replace(';', "_SEMCOL_")\
        .replace('!', "_EXCL_").replace('/', "_SLASH_")


def get_lists(tagger, text):
    """
    :param supervised_train_data: list of tuples (word, tag)
    :return: lists of words, tags and rules
    """
    # tag_list = tagger._states
    # lexic = tagger._symbols

    # here you can choose between several way to tag the text, with the .tag(text), .best_path(text) or .best_path_simple(text) (see https://www.nltk.org/api/nltk.tag.hmm.html for more explanations)
    tag_list = tagger.best_path_simple(text)

    tag_list = list(set(tag_list))
    lexic = list(set(text))
    print(tag_list, lexic)

    # Create rule list
    rule_list = []
    for t1 in tag_list:
        for t2 in tag_list:
            prob = tagger._transitions[t1].prob(t2)
            logprob = -tagger._transitions[t1].logprob(t2)
            if prob != 0.0:
                rule_list.append(Rule(clean(t1), clean(t2), prob, logprob))
    if type(text[0]) != 'tuple':
        text = [(word, '') for word in text]
    # Create word list
    word_list = []
    prev_word = "BEG"
    for (word, _) in text:
        for tag in tag_list:
            prob = tagger._outputs[tag].prob(word)
            logprob = -tagger._output_logprob(word, tag)
            w = Word(clean(word), clean(tag), prev_word, prob, logprob)
            if prob != 0.0:
                word_list.append(w)
            prev_word = w

    word_list.sort(key=lambda x: x.text)
    print([tag_list, rule_list, word_list])
    return [tag_list, rule_list, word_list]
