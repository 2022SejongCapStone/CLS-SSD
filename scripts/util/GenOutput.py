import pickle
import random
import os

class GenOutput:
  def __init__(self):
    # output을 만들어내기 위한 하나의 dict(json) 생성
    self.output = {}
    pass
  

  def write(self, absolute_root_path:str):
    '''
    해당 객체의 dict(json)을 출력하기 위한 함수.

    absolute_root_path : (임시)CLS-SSD의 root 경로
    출력되는 json형식의 데이터는 absolute_root_path/system/test.p에 저장됨
    '''
    Npath = os.path.join(absolute_root_path, f"system/test.p")

    # dict 데이터는 pickle.dump로 덤프를 해서 저장함.
    with open(Npath, "wb") as f:
      pickle.dump(self.output, f, protocol=pickle.HIGHEST_PROTOCOL)
    
  def SelectRepresentationCluster(self, CloneList:list, LineIndex:int):
    # CloneList는 LineIndex줄을 가지는 코드 그룹의 Group cluster들을 나타낸다.
    for Cluster in CloneList:
      # 우선 하나의 Group에 대한 대표 Fragment를 NULL으로 지정한다.
      RepresentationFragment = None

      # 만약 Cluster의 core부분이 없다면? 
      if len(Cluster.core) != 0:
        
        # @TODO 대표 Fragment 추출 알고리즘 추가
        # 현재는 그냥 random.choice로 하나를 뽑아냄.
        RepresentationFragment = random.choice(Cluster.core)
        self.output[LineIndex][RepresentationFragment.id] = dict()

        for coreInCluster in Cluster.core:
          self.output[LineIndex][RepresentationFragment.id] = {
            coreInCluster.id : [
              coreInCluster.file, coreInCluster.startline,
              coreInCluster.endline, coreInCluster.simhash
            ]
          }
      
      if len(Cluster.edge) != 0 and RepresentationFragment == None:
        RepresentationFragment = random.choice(Cluster.edge)
        self.output[LineIndex][RepresentationFragment.id] = list()

        for edgeInCluster in Cluster.edge:
          self.output[LineIndex][RepresentationFragment.id] = {
            edgeInCluster.id : [
              edgeInCluster.file, edgeInCluster.startline,
              edgeInCluster.endline, edgeInCluster.simhash
            ]
          }

  def ParseCloneSets(self, CloneSets:dict):
   
    for LineIndex in CloneSets.keys():
      if len(CloneSets[LineIndex]):
        self.output[LineIndex] = dict()
        self.SelectRepresentationCluster(CloneSets[LineIndex], LineIndex)
