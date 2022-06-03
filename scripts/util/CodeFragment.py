import collections
from Crypto.Util.number import bytes_to_long
from .log import logger
import re
import hashlib
import itertools

log = logger(False)

class CodeFragment:
  IndexBuilder = {}
  PrimaryKey = itertools.count()
  def __init__(self,file,endline,startline,content):
    self.file = file
    self.startline = startline
    self.endline = endline
    self.content = content
    self.id = next(CodeFragment.PrimaryKey)
    self.tokenizer()
    self.getSimHash()
  
  def tokenizer(self):
    seperator = "[ \t\n\r\f.]"
    self.tokenList = re.split(seperator,self.content)
    self.tokenList = list(filter(lambda x: x != '', self.tokenList))
    self.tokenFrequencyDict = collections.Counter(self.tokenList)

  def getSimHash(self):
    v = [0 for i in range(64)]
    # print(self.tokenFrequencyDict.items())
    for token, frequency in self.tokenFrequencyDict.items():
      hash = bytes_to_long(hashlib.sha256(token.encode()).digest()[:8]) # 64 bit hash in int  TO DO: implement efficient hash
      for i in range(64):
        bit = (hash>>i) & 1
        if bit:
          v[i] += frequency
        else:
          v[i] -= frequency

    self.simhash = 0
    lineCount = self.content.count("\n")
    for freqSum in v:
      if freqSum > 0:
        self.simhash = (self.simhash << 1) | 1
      else:
        self.simhash = (self.simhash << 1) | 0

    log.log("[CodeFragment] binary hash  : %s", format(hash, '#066b'))
    log.log("[CodeFragment] self.simhash : %s", format(self.simhash, '#066b'))

    if lineCount in self.IndexBuilder.keys():
      self.IndexBuilder[lineCount].add(self)
    else:
      self.IndexBuilder[lineCount] = set()
      self.IndexBuilder[lineCount].add(self)