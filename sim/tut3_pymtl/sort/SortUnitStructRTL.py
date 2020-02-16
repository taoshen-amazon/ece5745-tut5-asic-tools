#=========================================================================
# SortUnitStructRTL
#=========================================================================
# This model sorts four nbit elements into ascending order using a
# bitonic sorting network. We break the four elements into two pairs and
# sort each pair independently. Then we compare the smaller elements from
# each pair and the larger elements from each pair before arranging the
# middle two elements. This implementation uses structural composition of
# Reg and MinMax child models.

from pymtl3            import *
from pymtl3.stdlib.rtl import Reg, RegRst
from .MinMaxUnit       import MinMaxUnit

class SortUnitStructRTL( Component ):

  #=======================================================================
  # Constructor
  #=======================================================================

  def construct( s, nbits=8 ):

    DataType = mk_bits(nbits)

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.in_val  = InPort ()
    s.in_     = [ InPort (DataType) for _ in range(4) ]

    s.out_val = OutPort()
    s.out     = [ OutPort(DataType) for _ in range(4) ]

    #---------------------------------------------------------------------
    # Stage S0->S1 pipeline registers
    #---------------------------------------------------------------------

    s.val_S0S1 = RegRst(Bits1)( in_ = s.in_val )
    s.elm_S0S1 = [ Reg(DataType)( in_ = s.in_[i] ) for i in range(4) ]

    for i in range(4):
      s.elm_S0S1[i].in_ //= s.in_[i]

    #---------------------------------------------------------------------
    # Stage S1 combinational logic
    #---------------------------------------------------------------------

    s.minmax0_S1 = MinMaxUnit(DataType)(
      in0 = s.elm_S0S1[0].out,
      in1 = s.elm_S0S1[1].out,
    )

    s.minmax1_S1 = MinMaxUnit(DataType)(
      in0 = s.elm_S0S1[2].out,
      in1 = s.elm_S0S1[3].out,
    )

    #---------------------------------------------------------------------
    # Stage S1->S2 pipeline registers
    #---------------------------------------------------------------------

    s.val_S1S2 = RegRst(Bits1)( in_ = s.val_S0S1.out )
    s.elm_S1S2 = [ Reg(DataType) for _ in range(4) ]

    s.elm_S1S2[0].in_ //= s.minmax0_S1.out_min
    s.elm_S1S2[1].in_ //= s.minmax0_S1.out_max
    s.elm_S1S2[2].in_ //= s.minmax1_S1.out_min
    s.elm_S1S2[3].in_ //= s.minmax1_S1.out_max

    #----------------------------------------------------------------------
    # Stage S2 combinational logic
    #----------------------------------------------------------------------

    s.minmax0_S2 = MinMaxUnit(DataType)(
      in0 = s.elm_S1S2[0].out,
      in1 = s.elm_S1S2[2].out,
    )

    s.minmax1_S2 = MinMaxUnit(DataType)(
      in0 = s.elm_S1S2[1].out,
      in1 = s.elm_S1S2[3].out,
    )

    #----------------------------------------------------------------------
    # Stage S2->S3 pipeline registers
    #----------------------------------------------------------------------

    s.val_S2S3 = RegRst(Bits1)( in_ = s.val_S1S2.out )
    s.elm_S2S3 = [ Reg(DataType) for _ in range(4) ]

    s.elm_S2S3[0].in_ //= s.minmax0_S2.out_min
    s.elm_S2S3[1].in_ //= s.minmax0_S2.out_max
    s.elm_S2S3[2].in_ //= s.minmax1_S2.out_min
    s.elm_S2S3[3].in_ //= s.minmax1_S2.out_max

    #----------------------------------------------------------------------
    # Stage S3 combinational logic
    #----------------------------------------------------------------------

    s.minmax_S3 = MinMaxUnit(DataType)(
      in0 = s.elm_S2S3[1].out,
      in1 = s.elm_S2S3[2].out,
    )
    # Assign output ports

    s.out_val //= s.val_S2S3.out
    s.out[0]  //= s.elm_S2S3[0].out
    s.out[1]  //= s.minmax_S3.out_min
    s.out[2]  //= s.minmax_S3.out_max
    s.out[3]  //= s.elm_S2S3[3].out

  #=======================================================================
  # Line tracing
  #=======================================================================

  def line_trace( s ):

    def trace_val_elm( val, elm ):
      str_ = '{{{},{},{},{}}}'.format( elm[0], elm[1], elm[2], elm[3] )
      if not val:
        str_ = ' '*len(str_)
      return str_

    return "{}|{}|{}|{}|{}".format(
      trace_val_elm( s.in_val,        s.in_                         ),
      trace_val_elm( s.val_S0S1.out,  [ m.out for m in s.elm_S0S1 ] ),
      trace_val_elm( s.val_S1S2.out,  [ m.out for m in s.elm_S1S2 ] ),
      trace_val_elm( s.val_S2S3.out,  [ m.out for m in s.elm_S2S3 ] ),
      trace_val_elm( s.out_val,       s.out                         ),
    )

