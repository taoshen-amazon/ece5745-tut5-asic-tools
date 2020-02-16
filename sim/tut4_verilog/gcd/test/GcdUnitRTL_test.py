#=========================================================================
# GcdUnitRTL_test
#=========================================================================

import pytest

from pymtl3                    import *
from pymtl3.stdlib.test        import run_sim, config_model
from tut4_verilog.gcd.GcdUnitRTL import GcdUnitRTL

# Reuse tests from FL model

from .GcdUnitCL_test import TestHarness, test_case_table

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test_gcd_rtl( test_params, dump_vcd, test_verilog ):
  th = TestHarness( GcdUnitRTL() )

  th.set_param("top.tm.src.construct",
    msgs=test_params.msgs[::2],
    initial_delay=test_params.src_delay,
    interval_delay=test_params.src_delay )

  th.set_param("top.tm.sink.construct",
    msgs=test_params.msgs[1::2],
    initial_delay=test_params.sink_delay,
    interval_delay=test_params.sink_delay )

  config_model( th, dump_vcd, test_verilog, ['gcd'] )

  run_sim( th )
