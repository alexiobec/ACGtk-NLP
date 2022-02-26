import spacy
import numpy as np
import ngram as ng

test1 = "I play in a theater play"
test2 = "Bonjour! Je suis un test !J'ai été conçu pour être un test."

file = open("etranger.txt","r")
etranger = file.read().replace("¬\n","")
file.close()

nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")


class Word :
    def __init__(self, text, tag, upos, stop, dep) :
        self.text = text
        self.upos = upos
        self.tag = tag
        self.stop = stop
        self.dep = dep
        self.count = 1

    def plusplus(self):
        self.count += 1

    def __eq__ (self, other) :
        return(strEqual(self.text,other.text) & strEqual(self.tag,other.tag))

    def __str__(self):
        return(f"({self.text},{self.upos},{self.count})")

def strEqual (str1, str2) :
    if len(str1) == len(str2) :
        for i in range(len(str1)) :
            if str1[i] != str2[i] :
                return(False)
        return(True)
    else :
        return(False)


def count_tag(txt) :
    doc = nlp_fr(txt)
    wordArray = []
    for token in doc :
        word = Word(token.lemma_, token.tag_,token.pos_,token.is_stop, token.dep_)
        if word not in wordArray :
            wordArray.append(word)
        else :
            for w in wordArray :
                if w == word :
                    w.plusplus()
    return(wordArray)


     
print(count_tag(etranger))