#=========================================================================
# SortUnitStructRTL
#=========================================================================
# This model sorts four nbit elements into ascending order using a
# bitonic sorting network. We break the four elements into two pairs and
# sort each pair independently. Then we compare the smaller elements from
# each pair and the larger elements from each pair before arranging the
# middle two elements. This implementation uses structural composition of
# Reg and MinMax child models.

import os
from pymtl3 import *
from pymtl3.passes.backends.verilog import (
  VerilogPlaceholderConfigs,
  VerilatorImportConfigs,
  TranslationConfigs,
)
from .MinMaxUnit       import MinMaxUnit

class SortUnitStructRTL( Placeholder, Component ):

  # Constructor

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
    # Configurations
    #---------------------------------------------------------------------

    s.config_placeholder = VerilogPlaceholderConfigs(
      # Path to the Verilog source file
      src_file = os.path.dirname( __file__ ) + '/SortUnitStructRTL.v',
      # Name of the Verilog top level module
      top_module = 'tut4_verilog_sort_SortUnitStructRTL',
      # Parameters of the Verilog module
      params = { 'p_nbits' : nbits },
      # Port name map
      port_map = {
        'in_val'  : 'in_val',
        'in_[0]'  : 'in0',
        'in_[1]'  : 'in1',
        'in_[2]'  : 'in2',
        'in_[3]'  : 'in3',
        'out_val' : 'out_val',
        'out[0]'  : 'out0',
        'out[1]'  : 'out1',
        'out[2]'  : 'out2',
        'out[3]'  : 'out3',
      },
    )

    s.config_verilog_import = VerilatorImportConfigs(
      # Enable native Verilog line trace through Verilator
      vl_line_trace = False,
    )
    s.config_verilog_translate = TranslationConfigs(
      translate = False,
      explicit_module_name = f'SortUnitStructRTL_{nbits}bit',
    )
