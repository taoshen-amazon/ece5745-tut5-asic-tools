#=========================================================================
# SortUnitFlatRTL_v_test
#=========================================================================

from pymtl3                         import *
from pymtl3.passes.backends.verilog import VerilogPlaceholderPass, TranslationImportPass
from pymtl3.stdlib.test             import config_model
from .SortUnitFlatRTL               import SortUnitFlatRTL

def test_verilate( dump_vcd, test_verilog ):

  # Conflat the model

  model = SortUnitFlatRTL(8)

  # Configure the model

  config_model( model, dump_vcd, test_verilog )

  # Apply necessary passes

  model.apply ( VerilogPlaceholderPass() )
  model = TranslationImportPass()( model )

  # Create and reset simulator

  model.apply( SimulationPass() )
  model.sim_reset()
  print("")

  # Helper function

  def t( in_val, in_, out_val, out ):

    model.in_val = b1(in_val)
    for i,v in enumerate( in_ ):
      model.in_[i] = b8(v)

    model.eval_combinational()
    print( model.line_trace() )

    assert model.out_val == out_val
    if ( out_val ):
      for i,v in enumerate( out ):
        assert model.out[i] == v

    model.tick()

  # Cycle-by-cycle tests

  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )
  t( 1, [ 0x03, 0x09, 0x04, 0x01 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )
  t( 1, [ 0x10, 0x23, 0x02, 0x41 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )
  t( 1, [ 0x02, 0x55, 0x13, 0x07 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )
  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 1, [ 0x01, 0x03, 0x04, 0x09 ] )
  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 1, [ 0x02, 0x10, 0x23, 0x41 ] )
  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 1, [ 0x02, 0x07, 0x13, 0x55 ] )
  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )
  t( 0, [ 0x00, 0x00, 0x00, 0x00 ], 0, [ 0x00, 0x00, 0x00, 0x00 ] )

