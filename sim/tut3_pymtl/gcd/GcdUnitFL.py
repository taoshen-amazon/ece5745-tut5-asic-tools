#=========================================================================
# GCD Unit FL Model
#=========================================================================

from pymtl3      import *

def gcd_fl( a, b ):
  while True:
    if a < b:
      a, b = b, a
    elif b != 0:
      a = a - b
    else:
      return a
