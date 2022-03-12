import os
dirname = os.path.dirname(__file__)

def create_tag_sign(name,language,tag_list,rule_list,word_list):
    fichier = open(f"{dirname}/tag_sign/{name}_sign_tag_{language}.pacg", "w")
    fichier.write(str_tot(tag_list,rule_list,word_list))
    fichier.close()

def tag_type(tag_list) :
    str_tag ="\t"+str(tag_list[0])
    for tag in tag_list[1:] :
        str_tag += ',' + str(tag)
    return(str_tag+":type;\n\n")

def rule_tag(rule_list) :
    rules_str = ""
    for rule in rule_list :
        line = f"\t{str(rule.end)+ str(rule.count)}:{str(rule.beg)}->{str(rule.end)}[{str(rule.proba)}];\n"
        rule.count += 1
        rules_str += line
    return(rules_str + "\n")

def word_tag(word_list) :
    words_str =""
    for word in word_list :
        line = f"\t{word.text}:{word.tag}[{word.proba}];\n"
        words_str += line
    return(words_str+"\n")

def str_tot(tag_list,rule_list,word_list) :
    return(f"signature Syntax=\n\n{tag_type(tag_list)}{rule_tag(rule_list)}{word_tag(word_list)}end")
