import os
from util.CodeFragment import CodeFragment
from bs4 import BeautifulSoup as bf

class ICloneIndex:
  def __init__(self, output_path, rename):
    Npath = os.path.join(output_path, f"functions-{rename}.xml")
    self.extractFragments(Npath)
    self.extractedFragments = CodeFragment.IndexBuilder
  
  def extractFragments(self, XMLfile):
    '''
    XMLfile : functions.xml의 절대 경로

    expected return : 각 소스코드별 simhash가 담긴 객체 set
    '''
    
    with open(XMLfile, 'r', encoding='ISO-8859-1') as f:
      d = f.read()
      soup = bf(d, features="html.parser")

    for source in soup.findAll('source'): 
      _start = source['startline']
      _end = source['endline']
      _file = source['file']
      _content = source.next_sibling.strip()
      CodeFragment(_start, _end, _file, _content)