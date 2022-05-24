import os
dirname = os.path.dirname(__file__)


def create_str_sign(name, language, word_list):
    """
    :param name: name for the file 
    :param language: language of the text
    :param word_list: list of words
    :return: the string signature file
    """
    fichier = open(f"{dirname}/str_sign/{name}_sign_str_{language}.pacg", "w")
    fichier.write(str_tot(word_list))
    fichier.close()


def word_tag(word_list):
    """:return: the string used in the string signature file"""
    words_str = word_list[0].text
    prev = word_list[0]
    for word in word_list[1:]:
        if word.text != prev.text:
            if word.text[0] != prev.text[0]:
                words_str += "\n\n\t"
            else:
                words_str += ", "
            words_str += word.text
        prev = word
    return(words_str)


def str_tot(word_list):
    return(f"signature Strings=\n\n\to:type;\n\tstring=o->o: type;\n\tinfix +=lambda x y z.x(y z):string -> string -> string;\n\n\t{word_tag(word_list)}\n\t:string;\n\nend")
