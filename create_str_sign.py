import os
dirname = os.path.dirname(__file__)

def create_str_sign(name,language,word_list):
    fichier = open(f"{dirname}/str_sign/{name}_sign_str_{language}.pacg", "w")
    fichier.write(str_tot(word_list))
    fichier.close()


def word_tag(word_list) :
    words_str = word_list[0].text
    for word in word_list[1:] :
        words_str += f",{word.text}"
    return(words_str)

def str_tot(word_list) :
    return(f"signature Strings=\n\n\to:type;\n\tstring=o->o: type;\n\tinfix +=lambda x y z.x(y z):string -> string -> string;\n\t{word_tag(word_list)}:string;\nend")