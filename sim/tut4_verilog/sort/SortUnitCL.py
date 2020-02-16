#=========================================================================
# Sort Unit CL Model
#=========================================================================
# Models the cycle-approximate timing behavior of the target hardware.

from collections import deque

from pymtl3       import *

from .SortUnitFL import sort_fl

class SortUnitCL( Component ):

  # Constructor

  def construct( s, nbits=8, nstages=3 ):
    DataType = mk_bits( nbits )

    s.in_val = InPort ()
    s.in_    = [ InPort (DataType) for _ in range(4) ]

    s.out_val = OutPort()
    s.out     = [ OutPort(DataType) for _ in range(4) ]

    s.pipe    = deque( [None]*(nstages-1) )

    @s.update_ff
    def block():
      s.pipe.appendleft( sort_fl(s.in_) if s.in_val else None )

      if s.pipe[-1] is None:
        s.out_val <<= b1(0)
        for i in range(4):
          s.out[i] <<= DataType(0)
      else:
        s.out_val <<= b1(1)
        for i, v in enumerate( s.pipe[-1] ):
          s.out[i] <<= v
      s.pipe.pop()

  # Line tracing

  def line_trace( s ):

    in_str = '{' + ','.join(map(str,s.in_)) + '}'
    if not s.in_val:
      in_str = ' '*len(in_str)

    out_str = '{' + ','.join(map(str,s.out)) + '}'
    if not s.out_val:
      out_str = ' '*len(out_str)

    return "{}|{}".format( in_str, out_str )

