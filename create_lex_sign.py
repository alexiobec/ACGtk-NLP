import os
dirname = os.path.dirname(__file__)


def create_lexic(name, language, rule_list, word_list):
    """
    :param name: name for the file to create, it will be of the form "name"_lexic_"language".pacg
    :param language: language of the sentences
    :param rule_list: list of rules
    :param word_list: list of words
    :return: the lexicon file
    """
    fichier = open(f"{dirname}/lex_sign/{name}_lexic_{language}.pacg", "w")
    fichier.write(str_tot(name, rule_list, word_list))
    fichier.close()


def tag_def(tag_list):
    """
    :param tag_list: list of tags
    :return: the "tag string" to create the lexicon 
    """
    str_tag = "\t"+str(tag_list[0])
    for tag in tag_list[1:]:
        str_tag += ',' + str(tag)
    return(str_tag+":=string;\n\n")


def rule_def(rule_list):
    """
    :param rule_list: list of rules
    :return: the "rule string" to create the lexicon
    """
    rules_str = "\t"
    for rule in rule_list:
        rules_str += str(rule.beg) + str(rule.end) + ","
    rules_str = rules_str[:-1]+":=lambda xy.x+y;\n"
    return(rules_str + "\n")


def word_def(word_list):
    """
    :param word_list: list of the words
    :return: the "word string" to create the lexicon
    """
    words_str = ""
    memory = []
    for word in word_list:
        if word.prev == "BEG":
            # if [word.text, word.tag] not in memory:
            line = f"\tstart_{word.text}_{word.tag}:={word.text}\n"
            #memory.append([word.text, word.tag])
        else:
            # f [word.prev.tag, word.text, word.tag] not in memory:
            line = f"\t{word.prev.tag}_{word.text}_{word.tag}:={word.text}\n"
            #memory.append([word.prev.tag, word.text, word.tag])

        words_str += line
    return(words_str+"\n")


def str_tot(name, rule_list, word_list):
    """
    :param name: name for the file to create, it will be of the form "name"_lexic.pacg
    :param rule_list: list of rules
    :param word_list: list of words
    :return: the lexicon file
    """
    return(f"{name}_lexic:Strings =\n\n{rule_def(rule_list)}{word_def(word_list)}end")
