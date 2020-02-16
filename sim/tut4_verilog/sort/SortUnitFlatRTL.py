#=========================================================================
# SortUnitFlatRTL
#=========================================================================
# A register-transfer-level model explicitly represents state elements
# with s.tick concurrent blocks and uses s.combinational concurrent
# blocks to model how data transfers between state elements.

import os
from pymtl3 import *
from pymtl3.passes.backends.verilog import (
  VerilogPlaceholderConfigs,
  VerilatorImportConfigs,
  TranslationConfigs,
)

class SortUnitFlatRTL( Placeholder, Component ):

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
    # Configurations
    #---------------------------------------------------------------------

    s.config_placeholder = VerilogPlaceholderConfigs(
      # Path to the Verilog source file
      src_file = os.path.dirname( __file__ ) + '/SortUnitFlatRTL.v',
      # Name of the Verilog top level module
      top_module = 'tut4_verilog_sort_SortUnitFlatRTL',
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
    s.config_verilog_translate = TranslationConfigs(
      translate = False,
      explicit_module_name = f'SortUnitFlatRTL_{nbits}bit',
    )
