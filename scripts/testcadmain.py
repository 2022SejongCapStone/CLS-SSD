#!/bin/python3
from lib2to3.pgen2 import token
from bs4 import BeautifulSoup as bf
import re
import hashlib
from operator import countOf
import collections
from Crypto.Util.number import bytes_to_long, long_to_bytes

class CodeFragment:
    def __init__(self,file,endline,startline,content):
        self.file = file
        self.startline = startline
        self.endline = endline
        self.content = content
        self.tokenizer()
        self.getSimHash()
    
    def tokenizer(self):
        seperator = "[ \t\n\r\f.]"
        self.tokenList = re.split(seperator,self.content)
        self.tokenList = list(filter(lambda x: x != '', self.tokenList))
        self.tokenFrequencyDict = collections.Counter(self.tokenList)



    
    # def createTokenHashMap(self):
    #     self.tokenHashMap = {}
    #     for token in self.tokenList:
    #         hash = hashlib.sha256(self.content.encode()).digest()[:8] # 64 bit hash in bytes
    #         self.tokenHashMap[hash] = token
        
    def getSimHash(self):
        v = [0 for i in range(64)]      
        for token, frequency in self.tokenFrequencyDict.items():
            hash = bytes_to_long(hashlib.sha256(token.encode()).digest()[:8]) # 64 bit hash in int  TO DO: implement efficient hash
            for i in range(64):
                bit = (hash>>i) & 1
                if bit:
                    v[i] += frequency
                else:
                    v[i] -= frequency
        
        self.simhash = 0
        for freqSum in v:
            if freqSum > 0:
                self.simhash += 1
            self.simhash <<= 1
        
def getHammingDistance(simhash1, simhash2):
    xor = simhash1^simhash2
    hamming = bin(xor).count('1')  # TO DO : use lookup table for this
    return hamming


file = "system/test_functions-consistent.xml"
with open(file, 'r') as f:
    soup = bf(f, features="html.parser")


lst = []
for source in soup.findAll('source'):
    _start = source['startline']
    _end = source['endline']
    _file = source['file']
    _content = source.next_sibling.strip()
    lst.append(CodeFragment(_start, _end, _file, _content))


# for codeFrag in lst:
#     print(codeFrag.tokenList)
#     print(bin(codeFrag.simhash))

print(getHammingDistance(lst[0].simhash,lst[1].simhash))
print(getHammingDistance(lst[-4].simhash,lst[-5].simhash))
print(getHammingDistance(lst[-2].simhash,lst[-1].simhash))

