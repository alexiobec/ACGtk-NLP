import os
dirname = os.path.dirname(__file__)


def create_tag_sign(name, language, tag_list, rule_list, word_list, typeprob):
    """
    :param name: name for the file
    :param language: language of the text
    :param tag_list: list of tags
    :param rule_list: list of rules
    :param word_list: list of words
    :param typeprob: type of probability, logprob, prob or hidden
    """
    file = open(f"{dirname}/tag_sign/{name}_sign_tag_{language}.pacg", "w")
    file.write(str_tot(tag_list, rule_list, word_list, typeprob))
    file.close()


def tag_type(tag_list):
    """ :return: a string used in the tag file """
    str_tag = "\t"+str(tag_list[0])
    for tag in tag_list[1:]:
        str_tag += ',' + str(tag)
    return(str_tag+":type;\n\n")


def rule_tag(word_list, rule_list, typeprob):
    """ :return: a string used in the tag file """
    rules_str = ""
    for word in word_list:
        if word.prev == "BEG":
            for rule in rule_list:
                if rule.beg == "BEG" and rule.end == word.tag:
                    line = f"\tBEG_{word.text}_{word.tag}:={word.text}-> {rule.end}"
                    if typeprob == 'logprob':
                        line += f"[{rule.logproba+word.logproba}]"
                    elif typeprob == 'prob':
                        line += f"[{rule.proba*word.proba}]"
                    line += ";\n"
        else:
            for rule in rule_list:
                if rule.beg == word.prev.tag and rule.end == word.tag:
                    line = f"\t{word.prev.tag}_{word.text}_{word.tag}:={word.text}-> {str(rule.end)}"
                    if typeprob == 'log':
                        line += f"[{str(rule.logproba+word.logproba)}]"
                    elif typeprob == 'prob':
                        line += f"[{str(rule.proba*word.proba)}]"
                    line += ";\n"
        rules_str += line
    return(rules_str + "\n")


def word_tag(word_list, typeprob):
    """ :return: a string used in the tag file """
    words_str = ""
    for word in word_list:
        words_str += f"\t{word.text}:{word.tag}"
        if typeprob == 'logprob':
            words_str += f"[{str(word.logproba)}]"
        elif typeprob == 'prob':
            words_str += f"[{str(word.proba)}]"
        words_str += ";\n"
    return(words_str+"\n")


def str_tot(tag_list, rule_list, word_list, typeprob):
    return(f"signature Syntax=\n\n{tag_type(tag_list)}{rule_tag(word_list,rule_list,typeprob)}{word_tag(word_list,typeprob)}end")
