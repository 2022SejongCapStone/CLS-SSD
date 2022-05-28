#!/usr/bin/python3

'''
CLS-SSD Analysis part

Support OS : Linux

우선 소스코드에 있는 코드들을 xml로 만든 후( Using ExtractAndRename ),
해당 파일의 코드들의 simhash를 DBSCAN으로 그룹지어 cluster를 만든 후
각 cluster 중 대표를 xml 파일로 출력한다.

Execution
  python3 ./scripts/analysis.py c function 123 group /path/to/source /path/to/output

argv
  1 - language          = default c ( @TODO py, java, cs ... )
  2 - granularity       = default funtion ( @TODO block )
  3 - clone_type        = default 123 ( @TODO 1|2|3 )
  4 - clone_grouping    = default group ( @TODO pair )
  5 - source_path       = absolute path to source folder
  6 - output_path       = absolute path to output folder
'''

import os
import sys
import subprocess
from util.log import logger

absolute_root_path = ""

def usage():
  print("Execution")
  print("python3 ./scripts/analysis.py c function 123 blind generous /path/to/source /path/to/output")
  print("  ")
  print("argv")
  print("1 - language          = default c ( @TODO py, java, cs ... )")
  print("2 - granularity       = default funtion ( @TODO block )")
  print("3 - clone_type        = default 123 ( @TODO 1|2|3 )")
  print("4 - clone_grouping    = default group ( @TODO pair )")
  print("5 - source_transform  = default generous or blind")
  print("6 - source_path       = absolute path to source folder")
  print("7 - output_path       = absolute path to output folder")

def main():
  global absolute_root_path
  absolute_analysis_path = os.path.dirname(os.path.abspath(__file__))
  absolute_root_path = os.path.abspath(os.path.join(absolute_analysis_path, ".."))
  print(absolute_root_path)

  if len(sys.argv) < 7:
    usage()
    return
  
  language = sys.argv[1]
  granularity = sys.argv[2]
  clone_type = sys.argv[3]
  clone_grouping = sys.argv[4]
  rename = "consistent" if sys.argv[5] == "generous" else "blind"
  source_path = sys.argv[6]
  output_path = sys.argv[7]

  log = logger(True)
  log.log("Argument")
  log.log("  language         : %s", language)
  log.log("  granularity      : %s", granularity)
  log.log("  clone_type       : %s", clone_type)
  log.log("  clone_grouping   : %s", clone_grouping)
  log.log("  rename           : %s", rename)
  log.log("  source_path      : %s", source_path)
  log.log("  output_path      : %s", output_path)
  
  # source data extraction
  # Using ExtractAndRename
  #   ./scripts/ExtractAndRename function c blind source_path output_path
  # output
  #   functions-blind.xml | functions.xml in `output_path`
  
  res = os.system(f"{absolute_root_path}/scripts/ExtractAndRename {language} {granularity} {rename} {source_path} {output_path}")
  print(res)


  # Parsing CodeFragment And update Simhash

  '''

  '''

  # DBSCAN in CodeFragments``


  # Export one code in each Groups





if __name__ == '__main__':

  main()