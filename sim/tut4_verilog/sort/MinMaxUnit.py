#=========================================================================
# MinMaxUnit
#=========================================================================
# This module takes two inputs, compares them, and outputs the larger
# via the "max" output port and the smaller via the "min" output port.

import os
from pymtl3 import *
from pymtl3.passes.backends.verilog import (
  VerilogPlaceholderConfigs,
  VerilatorImportConfigs,
  TranslationConfigs,
)

class MinMaxUnit( Placeholder, Component ):

  # Constructor

  def construct( s, DataType ):

    # Port-based interface

    s.in0     = InPort ( DataType )
    s.in1     = InPort ( DataType )
    s.out_min = OutPort( DataType )
    s.out_max = OutPort( DataType )

    # Configurations

    s.config_placeholder = VerilogPlaceholderConfigs(
      # Path to the Verilog source file
      src_file = os.path.dirname( __file__ ) + '/MinMaxUnit.v',
      # Name of the Verilog top level module
      top_module = 'tut4_verilog_sort_MinMaxUnit',
      # MinMaxUnit does not have clk and reset pins
      has_clk   = False,
      has_reset = False,
      # Verilog Parameters
      params = { 'p_nbits' : DataType.nbits },
    )
    s.config_verilog_translate = TranslationConfigs(
      translate = False,
      explicit_module_name = 'MinMaxUnit',
    )
