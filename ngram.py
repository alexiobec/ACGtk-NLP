import numpy as np

file = open("etranger.txt","r")
etranger = file.read().replace("¬\n","")
file.close()




def sparse(text) :
    i = 0
    Newtext = text.lower()
    while i < len(Newtext) :
        lettre = Newtext[i]
        if lettre in {".",",","!","?"}:
            Newtext = Newtext[:i] + " " + lettre + " " + Newtext[i+1:]
            i += 2
        elif lettre == "'" :
            Newtext = Newtext[:i+1] + " " + Newtext[i+1:]
            i += 1
        i+=1
    Newtext = Newtext.split()
    return(Newtext)

def unigram(text) :
    wordList = sparse(text)
    wordDict = {}
    for word in wordList :
        if word in wordDict :
            wordDict[word] += 1
        else :
            wordDict[word] = 1
    return(wordDict)

def bigram(text):
    sparsedText = sparse(text)
    wordList = []
    
    for word in sparsedText :
        if word not in wordList :
            wordList.append(word)

    n = len(wordList)
    matrix = np.zeros(n*n).reshape([n,n])

    for index,word in enumerate(sparsedText) :
        if index == len(sparsedText)-1 :
            return(wordList, matrix)
        index1 = wordList.index(word)
        index2 = wordList.index(sparsedText[index+1])
        matrix[index1,index2] += 1
        
    return([wordList, matrix])

