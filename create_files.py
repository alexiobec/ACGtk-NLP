import create_lex_sign as _lex
import create_tag_sign as _tag
import create_str_sign as _str


class Rule :
    def __init__(self, tag_beg,tag_end,probability):
        self.beg = tag_beg
        self.end = tag_end
        self.proba = probability
        self.count = 1

class Word :
    def __init__(self,text,tag,previousWord,proba) :
        self.text = text
        self.tag = tag
        self.proba = proba
        self.prev = previousWord


def create_files(name,language,tag_list,rule_list,word_list,tag = True,str = True, lexic = True) :
    if lexic :
        _lex.create_lexic(name,language,tag_list,rule_list,word_list)
    if str :
        _str.create_str_sign(name,language,word_list)
    if tag :
        _tag.create_tag_sign(name,language,tag_list,rule_list,word_list)



#Phrase : "je mange une pomme"
rule1 = Rule("beg","sujet",1)
rule2 = Rule("sujet",'verbe',1)
rule3 = Rule('verbe',"article",1)
rule4 = Rule("article","nom",1)
rule5 = Rule("nom","_end_",1)

_beg_ = Word("_start_","beg",None,1)
wordJe = Word('je','sujet',_beg_,1)
wordMange = Word("mange",'verbe',wordJe,1)
wordUne = Word("une",'article',wordMange,1)
wordPomme = Word("pomme",'nom',wordUne,1)

tag_list = ["sujet",'verbe',"article","nom"]
rule_list = [rule1,rule2,rule3,rule4,rule5]
word_list = [wordJe,wordMange,wordUne,wordPomme]

create_files("test1","fr",tag_list,rule_list,word_list)
