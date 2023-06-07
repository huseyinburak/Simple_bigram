# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 19:43:33 2022

@author: HB_Onen
"""
import re

import codecs  

import numpy as np

import collections

from collections import Counter
############################################################

def tokenize(str):
    return tokenize2(str, r'[A-Za-z]+')

def tokenizeTurkish(str):
    return tokenize2(str, r'[A-Za-zığüşiöçIĞÜŞİÖÇ</>]+')


def tokenize2(str, wordPattern):
    return re.findall(wordPattern,str)

def readFile(fname):
    file = codecs.open(fname, encoding='utf-8')
    txt = file.read()
    txt = txt.lower()
    file.close()
    return txt

def sentenceCounter(txt):
    sentenceCount = 0;
    for x in txt:
        if ((x == ".") or (x == "?") or (x == "!")):  sentenceCount += 1;
    return sentenceCount

def vocabulary(str):
    vocab = set()
    for t in str:
             #tL = t.lower()
             vocab.add(t)
    return vocab

def replacement(str):
    str = "<s> " + str
    if(str.endswith(".") or str.endswith("?") or str.endswith("!")):
        str = str[:-1] 
        str = str + " </s>"
    str = str.replace(". ", " </s> <s> ")
    str = str.replace(".", " </s> <s> ")
    return str
##############################################################

filePath = 'D:\'
fname = filePath + 'bilgisayar.txt'
#fname = filePath + 'bilgisayar.txt'
txt = readFile(fname)

#print(txt + "\n")

sentenceCount = sentenceCounter(txt)

print('%s%d' %("Number of Sentences in File: ", sentenceCount) + "\n") 

txt = replacement(txt)

tokens = tokenizeTurkish(txt)
numTokens = len(tokens)
#print(tokens)
print("\n")


vocab = vocabulary(tokens)
numVocab = len(vocab)
#print(vocab)
print("\n")

frequency = collections.Counter(tokens)
sortedFreq = sorted(frequency.items(), key=lambda pair: pair[1], reverse=True)
freqOfToken = []
print("{0:25} {1:<20} {2}".format('Tokens','Frequency','Probabilities'))
for f in sortedFreq: 
    print("{0:25} {1:<20} {2}".format(f[0], f[1], int(f[1])/numTokens))
    freqOfToken.append(f[1])
  
bigrams = []
for i in range(len(tokens) - 1):
    bigramTuple = (tokens[i] , tokens[i+1])
    bigrams.append(bigramTuple)
 
freqBigram = collections.Counter(bigrams)    
sortedBigram = sorted(freqBigram.items(), key=lambda pair: pair[1], reverse=True)
probBigrams={}
#print("\n{0:25} {1:<20} {2}".format('Bigrams','Frequency','Probabilities'))
for b in sortedBigram:
    #print("{0:25} {1:<20} {2}".format(','.join(b[0]), b[1], b[1]/frequency[b[0][0]]))
    #probBigram = {','.join(b[0]) : b[1]/frequency[b[0][0]]}
    probBigrams[b[0]] = b[1]/frequency[b[0][0]]

minFreq = freqOfToken[numVocab - 1]
unkWord = []
for n in reversed(range(numVocab)):
    if sortedFreq[n][1] == minFreq: 
        unkWord.append(sortedFreq[n][0])
    else: break        
#print(unkWord)

tokenNp = np.array(tokens)
for unk in unkWord:
    tokenNp[(tokenNp == unk)]  = '<UNK>'
    
#print(tokenNp)

frequency = collections.Counter(tokenNp)
sortedFreq = sorted(frequency.items(), key=lambda pair: pair[1], reverse=True)
freqOfToken = []
#print("{0:25} {1:<20} {2}".format('Tokens','Frequency','Probabilities'))
for f in sortedFreq: 
    #print("{0:25} {1:<20} {2}".format(f[0], f[1], int(f[1])/numTokens))
    freqOfToken.append(f[1])

bigrams = []
for i in range(len(tokenNp) - 1):
    bigramTuple = (tokenNp[i] , tokenNp[i+1])
    bigrams.append(bigramTuple)
 
freqBigram = collections.Counter(bigrams)    
sortedBigram = sorted(freqBigram.items(), key=lambda pair: pair[1], reverse=True)
unkProbBigrams={}
print("\n{0:25} {1:<20} {2}".format('Bigrams','Frequency','Probabilities'))
for b in sortedBigram:
    print("{0:25} {1:<20} {2}".format(','.join(b[0]), b[1], b[1]/frequency[b[0][0]]))
    unkProbBigrams[b[0]] = b[1]/frequency[b[0][0]]
    
    
k=0.5  
smthUnkProbBigrams={}  
#print("\n{0:25} {1:<20} {2}".format('Bigrams','Frequency','Smooth Probabilities'))
for b in sortedBigram:
    #print("{0:25} {1:<20} {2}".format(','.join(b[0]), b[1], (b[1] + k)/(frequency[b[0][0]] + (k * numVocab))))    
    smthUnkProbBigrams[b[0]] = (b[1] + k)/(frequency[b[0][0]] + (k * numVocab))

"""
print("Please, write first sentence to calculate probabilities : ")
testSentence1 = input()
testSentence1 = testSentence1.lower()
print("\n"+ "Please, write second sentence to calculate probabilities : ")
testSentence2 = input()
testSentence2 = testSentence2.lower()
""" 

#testSentence1 = "Bilgisayar ile rastgele bir cümle kurdum."
testSentence1 = "Ali evden unuttuğu eşyaları alıp diğer eve gitti."
testSentence2 = "ABD'nin Asya Pasifik bölgesinde konsolide etmeye çalıştığı ittifak ağında cılız da olsa karşıt sesler yükseliyor."
testSentence1 = testSentence1.lower()
testSentence2 = testSentence2.lower()

testSentence1 = replacement(testSentence1)
testSentence2 = replacement(testSentence2)

tokenSent1 = tokenizeTurkish(testSentence1)
tokenSent2 = tokenizeTurkish(testSentence2)

vocabSent1 = vocabulary(tokenSent1)
vocabSent2 = vocabulary(tokenSent2)


for s in range(len(tokenSent1)):
    for snt in vocabSent1: 
        if (frequency[snt] == 0) and (tokenSent1[s] == snt): 
            tokenSent1[s] = "<UNK>"            

print(tokenSent1) 

bigramSnt1 = []
for i in range(len(tokenSent1) - 1):
    bigramSntTuple = (tokenSent1[i] , tokenSent1[i+1])
    bigramSnt1.append(bigramSntTuple)

setOfBigrams=set(bigrams)
probSnt1=[]
for bS in range(len(bigramSnt1)):
    for b in setOfBigrams:
        if ((bigramSnt1[bS][0] == b[0]) and (bigramSnt1[bS][1] == b[1])): 
            print(bigramSnt1[bS])
            probSnt1.append(smthUnkProbBigrams[bigramSnt1[bS]])
print(probSnt1) 
           
probabilityOfSentence1 = 1
for p in probSnt1:
    probabilityOfSentence1 *=p
print(probabilityOfSentence1)
