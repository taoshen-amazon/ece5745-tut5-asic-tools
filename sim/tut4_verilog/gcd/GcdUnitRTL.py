#=========================================================================
# GCD Unit RTL Model
#=========================================================================

import os
from pymtl3 import *
from pymtl3.stdlib.ifcs import MinionIfcRTL
from pymtl3.passes.backends.verilog import (
  VerilogPlaceholderConfigs,
  VerilatorImportConfigs,
  TranslationConfigs,
)

from .GcdUnitMsg  import GcdUnitMsgs

#=========================================================================
# GCD Unit RTL Model
#=========================================================================

class GcdUnitRTL( Placeholder, Component ):

  # Constructor

  def construct( s ):

    # Interface

    s.minion = MinionIfcRTL( GcdUnitMsgs.req, GcdUnitMsgs.resp )

    # Configurations

    s.config_placeholder = VerilogPlaceholderConfigs(
      # Path to the Verilog source file
      src_file = os.path.dirname( __file__ ) + '/GcdUnitRTL.v',
      # Name of the Verilog top level module
      top_module = 'tut4_verilog_gcd_GcdUnitRTL',
      # Port name map
      port_map = {
        'minion.req.en'   : 'req_en',
        'minion.req.rdy'  : 'req_rdy',
        'minion.req.msg'  : 'req_msg',
        'minion.resp.en'  : 'resp_en',
        'minion.resp.rdy' : 'resp_rdy',
        'minion.resp.msg' : 'resp_msg',
      },
    )

    s.config_verilog_import = VerilatorImportConfigs(
      # Enable native Verilog line trace through Verilator
      vl_line_trace = True,
    )
    s.config_verilog_translate = TranslationConfigs(
      translate = False,
      explicit_module_name = 'GcdUnitRTL',
    )
