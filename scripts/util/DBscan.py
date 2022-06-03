import collections
from .log import logger
from .Cluster import Cluster

log = logger(False)

class DBscan:
  def __init__(self, S:dict, eps:int=13, minPts:int=2):
    self.detectedCloneSets = {}
    self.S = S

    # S : dict
    for Index in sorted(self.S.keys()):
      # 각 인덱스(line)별로 Group을 넣을 리스트를 생성함
      log.log("[DBscan __init__] Index : %d", Index)
      self.detectedCloneSets[Index] = []

      self.DBscan(self.S[Index], Index, eps, minPts)

  def getHammingDistance(self, simhash1, simhash2):
    xor = simhash1^simhash2
    hamming = bin(xor).count('1')
    return hamming

  def DBscan(self, S:set, Index, eps, minPts):
    '''
    @  S : Index의 줄을 가진 코드의 집합
    @  eps : 13( default )
    @  minPts : 2( default )

    Output
    @  self.detectedCloneSets 에 그룹별로 포함될 예정.
    '''

    # 방문 여부 집합
    visited = set()

    # 그룹 인덱스 번호
    self.cloneSetIndex = 0

    # BFS 탐색을 통해 Group을 묶어낸다.

    # queue를 만들어준다.
    Q = collections.deque()

    # 탐색 범위는 S 집합에 있는 원소들로 고정.
    for Fragment in S:

      # 우선 새로운 클러스터 하나를 만든다.
      newCluster = Cluster()

      # 방문했으면 continue
      if Fragment in visited:
        continue

      # 현재 코드 Fragment를 Queue에 추가함.
      Q.append(Fragment)
      visited.add(Fragment)
      
      # Queue가 empty가 될 때까지 반복
      while len(Q):

        # Queue에 있는 코드 Fragment 하나를 가져온다.
        FragmentInNeighbor = Q.popleft()

        # minPts에 포함되는 서로 다른 Fragment의 수를 셀 Count 변수
        Count = 0

        # Fragment 집합 S에서 다른 코드들을 확인하는 과정
        # 전수 조사
        for FragmentInGroup in S:
          if self.getHammingDistance(FragmentInNeighbor.simhash, FragmentInGroup.simhash) <= eps:
            # 거리가 eps 보다 작은 경우 Count는 늘리되,
            # 방문하지 않은 Fragment만 Queue에 추가한다.
            Count += 1
            if not FragmentInGroup in visited:
              Q.append(FragmentInGroup)
              visited.add(FragmentInGroup)
      
        # eps 이하인 다른 Fragment가 minPts개 이상일 경우
        # `core`에 추가한다.
        if Count >= minPts:
          newCluster.core.append(FragmentInNeighbor)

        # 만약 eps 이하인 다른 Fragment가 minPts개 미만이고
        # 0이 아니라면 ( 0 < Count < minPts )
        # `edge` 그룹에 추가한다.
        elif Count != 0:
          newCluster.edge.append(FragmentInNeighbor)
        
        # eps안에 어떤 Fragment도 없는 outlier Fragment는
        # Cluster에서 제외된다( 포함시키지 않음 ).
      
      # 한번 Queue를 넣고 반복을 돌렸을 때 나온 Cluster 하나를
      # Index(line)의 새로운 그룹으로 추가한다.

      self.detectedCloneSets[Index].append(newCluster)