import os
dirname = os.path.dirname(__file__)

def create_lexic(name,language,tag_list,rule_list,word_list):
    fichier = open(f"{dirname}/lex_sign/{name}_lexic_{language}.pacg", "w")
    fichier.write(str_tot(tag_list,rule_list,word_list))
    fichier.close()

def tag_def(tag_list) :
    str_tag ="\t"+str(tag_list[0])
    for tag in tag_list[1:] :
        str_tag += ',' + str(tag)
    return(str_tag+":=string;\n\n")

def rule_def(rule_list) :
    rules_str = "\t"
    for rule in rule_list :
        for i in range(rule.count) :
            rules_str += str(rule.end) + str(rule.count) +","
    rules_str = rules_str [:-1]+":=lambda xy.x+y;\n"
    return(rules_str + "\n")

def word_def(word_list) :
    words_str =""
    for word in word_list :
        line = f"\t{word.prev.tag}_{word.text}_{word.tag}:={word.text}\n"
        words_str += line
    return(words_str+"\n")

def str_tot(tag_list,rule_list,word_list) :
    return(f"lexicon:Strings =\n\n{tag_def(tag_list)}{rule_def(rule_list)}{word_def(word_list)}end")
