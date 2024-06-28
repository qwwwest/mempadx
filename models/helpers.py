
import os

class Helpers:
    
  @staticmethod
  def dirname(filename) :
    return os.path.dirname(os.path.realpath(filename))

  @staticmethod
  def readFile(filename) :
    "read file"  
    f = open(filename, 'r', encoding='utf-8')
    str = f.read()
    f.close()  
    return str