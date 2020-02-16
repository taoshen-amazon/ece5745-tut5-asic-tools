#=========================================================================
# Sort Unit CL Model
#=========================================================================
# Models the cycle-approximate timing behavior of the target hardware.

from collections import deque

from pymtl3       import *

class SortUnitCL( Component ):

  # Constructor

  def construct( s, nbits=8, nstages=3 ):
    DataType = mk_bits( nbits )

    s.in_val = InPort ()
    s.in_    = [ InPort (DataType) for _ in range(4) ]

    s.out_val = OutPort()
    s.out     = [ OutPort(DataType) for _ in range(4) ]

    s.pipe    = deque( [ [b1(0)] + [DataType(0) for _ in range(4)] ] * (nstages-1) )

    @s.update_ff
    def block():
      s.pipe.append( [ s.in_val ] + sorted(s.in_) )
      data = s.pipe.popleft()
      s.out_val <<= data[0]
      for i, v in enumerate( data[1:] ):
        s.out[i] <<= v

  # Line tracing

  def line_trace( s ):

    in_str = '{' + ','.join(map(str,s.in_)) + '}'
    if not s.in_val:
      in_str = ' '*len(in_str)

    out_str = '{' + ','.join(map(str,s.out)) + '}'
    if not s.out_val:
      out_str = ' '*len(out_str)

    return "{}|{}".format( in_str, out_str )

