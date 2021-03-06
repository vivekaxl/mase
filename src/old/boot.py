from __future__ import print_function,division
from functools import wraps
import traceback

"""

# Boot: Core utilities

"""

class o:
  def __init__(i,**d)    : i.__dict__.update(**d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k] 

the = o()

def setting(f):
  name = f.__name__
  @wraps(f)
  def wrapper(**d):
    tmp = f()
    tmp.update(**d)
    the[name] = tmp
    return tmp
  wrapper()
  return wrapper

def ok(*lst):
  for one in lst: unittest(one)
  return one

class unittest:
  tries = fails = 0  #  tracks the record so far
  @staticmethod
  def score():
    t = unittest.tries
    f = unittest.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print(traceback.format_exc())
    print(unittest.score(),':',test.__name__, e)
