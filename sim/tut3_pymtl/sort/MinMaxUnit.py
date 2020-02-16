#=========================================================================
# MinMaxUnit
#=========================================================================
# This module takes two inputs, compares them, and outputs the larger
# via the "max" output port and the smaller via the "min" output port.

from pymtl3 import *

class MinMaxUnit( Component ):

  # Constructor

  def construct( s, DataType ):

    s.in0     = InPort ( DataType )
    s.in1     = InPort ( DataType )
    s.out_min = OutPort( DataType )
    s.out_max = OutPort( DataType )

    # ''' TUTORIAL TASK ''''''''''''''''''''''''''''''''''''''''''''''''''
    # This model is incomplete. As part of the tutorial you will insert
    # logic here to implement the min/max unit. You should also write a
    # unit test from scratch named MinMaxUnit_test.py.
    # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

