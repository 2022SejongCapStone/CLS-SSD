
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class logger(bcolors):

  def __init__(self, flag):
    self.flag = flag
  
  def log(self, format, *args):
    if self.flag:
      print("[log.py]", self.HEADER + self.WARNING, format%args, self.ENDC)