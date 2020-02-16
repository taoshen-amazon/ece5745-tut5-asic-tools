#=========================================================================
# GCD Unit RTL Model
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.ifcs import MinionIfcRTL
from pymtl3.stdlib.rtl  import Mux, RegEn, RegRst
from pymtl3.stdlib.rtl  import LTComparator, ZeroComparator, Subtractor

from .GcdUnitMsg  import GcdUnitMsgs

#=========================================================================
# Constants
#=========================================================================

A_MUX_SEL_NBITS = 2
A_MUX_SEL_IN    = 0
A_MUX_SEL_SUB   = 1
A_MUX_SEL_B     = 2
A_MUX_SEL_X     = 0

B_MUX_SEL_NBITS = 1
B_MUX_SEL_A     = 0
B_MUX_SEL_IN    = 1
B_MUX_SEL_X     = 0

#=========================================================================
# GCD Unit RTL Datapath
#=========================================================================

class GcdUnitDpathRTL(Component):

  # Constructor

  def construct( s ):

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.req_msg_a = InPort (Bits16)
    s.req_msg_b = InPort (Bits16)
    s.resp_msg  = OutPort(Bits16)

    # Control signals (ctrl -> dpath)

    s.a_mux_sel = InPort( mk_bits(A_MUX_SEL_NBITS) )
    s.a_reg_en  = InPort()
    s.b_mux_sel = InPort( mk_bits(B_MUX_SEL_NBITS) )
    s.b_reg_en  = InPort()

    # Status signals (dpath -> ctrl)

    s.is_b_zero = OutPort()
    s.is_a_lt_b = OutPort()

    #---------------------------------------------------------------------
    # Structural composition
    #---------------------------------------------------------------------

    # A mux

    s.sub_out   = Wire(Bits16)
    s.b_reg_out = Wire(Bits16)

    s.a_mux = Mux( Bits16, 3 )(
      sel = s.a_mux_sel,
      in_ = { A_MUX_SEL_IN:  s.req_msg_a,
              A_MUX_SEL_SUB: s.sub_out,
              A_MUX_SEL_B:   s.b_reg_out }
    )

    # A register

    s.a_reg = RegEn(Bits16)(
      en  = s.a_reg_en,
      in_ = s.a_mux.out,
    )

    # B mux

    s.b_mux = Mux( Bits16, 2 )(
      sel = s.b_mux_sel,
      in_ = { B_MUX_SEL_A : s.a_reg.out,
              B_MUX_SEL_IN: s.req_msg_b }
    )

    # B register

    s.b_reg = RegEn(Bits16)(
      en  = s.b_reg_en,
      in_ = s.b_mux.out,
      out = s.b_reg_out,
    )

    # Zero compare

    s.b_zero = ZeroComparator(Bits16)(
      in_ = s.b_reg.out,
      out = s.is_b_zero,
    )

    # Less-than comparator

    s.a_lt_b = LTComparator(Bits16)(
      in0 = s.a_reg.out,
      in1 = s.b_reg.out,
      out = s.is_a_lt_b,
    )

    # Subtractor

    s.sub = Subtractor(Bits16)(
      in0 = s.a_reg.out,
      in1 = s.b_reg.out,
      out = s.sub_out,
    )

    # connect to output port

    s.resp_msg //= s.sub.out

#=========================================================================
# GCD Unit RTL Control
#=========================================================================

class GcdUnitCtrlRTL(Component):

  def construct( s ):

    #---------------------------------------------------------------------
    # Interface
    #---------------------------------------------------------------------

    s.req_en     = InPort ()
    s.req_rdy    = OutPort()

    s.resp_en   = OutPort()
    s.resp_rdy   = InPort ()

    # Control signals (ctrl -> dpath)

    s.a_mux_sel = OutPort( mk_bits(A_MUX_SEL_NBITS) )
    s.a_reg_en  = OutPort()
    s.b_mux_sel = OutPort()
    s.b_reg_en  = OutPort()

    # Status signals (dpath -> ctrl)

    s.is_b_zero = InPort( mk_bits(B_MUX_SEL_NBITS) )
    s.is_a_lt_b = InPort()

    # State element

    s.STATE_IDLE = b2(0)
    s.STATE_CALC = b2(1)
    s.STATE_DONE = b2(2)

    s.state = Wire( Bits2 )

    #---------------------------------------------------------------------
    # State Transition Logic
    #---------------------------------------------------------------------

    @s.update_ff
    def state_transitions():
      if s.reset:
        s.state <<= s.STATE_IDLE

      # Transistions out of IDLE state

      if s.state == s.STATE_IDLE:
        if s.req_en:
          s.state <<= s.STATE_CALC

      # Transistions out of CALC state

      if s.state == s.STATE_CALC:
        if not s.is_a_lt_b and s.is_b_zero:
          s.state <<= s.STATE_DONE

      # Transistions out of DONE state

      if s.state == s.STATE_DONE:
        if s.resp_rdy:
          s.state <<= s.STATE_IDLE

    #---------------------------------------------------------------------
    # State Output Logic
    #---------------------------------------------------------------------

    s.do_swap = Wire()
    s.do_sub  = Wire()

    @s.update
    def state_outputs():

      s.do_swap   = b1(0)
      s.do_sub    = b1(0)
      s.req_rdy   = b1(0)
      s.resp_en   = b1(0)
      s.a_mux_sel = b2(0)
      s.a_reg_en  = b1(0)
      s.b_mux_sel = b1(0)
      s.b_reg_en  = b1(0)

      # In IDLE state we simply wait for inputs to arrive and latch them

      if s.state == s.STATE_IDLE:
        s.req_rdy   = b1(1)
        s.resp_en   = b1(0)
        s.a_mux_sel = b2(A_MUX_SEL_IN)
        s.a_reg_en  = b1(1)
        s.b_mux_sel = b1(B_MUX_SEL_IN)
        s.b_reg_en  = b1(1)

      # In CALC state we iteratively swap/sub to calculate GCD

      elif s.state == s.STATE_CALC:

        s.do_swap = s.is_a_lt_b
        s.do_sub  = ~s.is_b_zero

        s.req_rdy   = b1(0)
        s.resp_en   = b1(0)
        s.a_mux_sel = b2(A_MUX_SEL_B) if s.do_swap else b2(A_MUX_SEL_SUB)
        s.a_reg_en  = b1(1)
        s.b_mux_sel = b1(B_MUX_SEL_A)
        s.b_reg_en  = s.do_swap

      # In DONE state we simply wait for output transaction to occur

      elif s.state == s.STATE_DONE:
        s.req_rdy   = b1(0)
        s.resp_en   = s.resp_rdy
        s.a_mux_sel = b2(A_MUX_SEL_X)
        s.a_reg_en  = b1(0)
        s.b_mux_sel = b1(B_MUX_SEL_X)
        s.b_reg_en  = b1(0)

#=========================================================================
# GCD Unit RTL Model
#=========================================================================

class GcdUnitRTL( Component ):

  # Constructor

  def construct( s ):

    # Interface

    s.minion = MinionIfcRTL( GcdUnitMsgs.req, GcdUnitMsgs.resp )

    # Instantiate datapath and control

    s.dpath = GcdUnitDpathRTL()(
      req_msg_a = s.minion.req.msg.a,
      req_msg_b = s.minion.req.msg.b,
      resp_msg  = s.minion.resp.msg,
    )

    s.ctrl  = GcdUnitCtrlRTL()(
      req_en   = s.minion.req.en,
      req_rdy  = s.minion.req.rdy,
      resp_en  = s.minion.resp.en,
      resp_rdy = s.minion.resp.rdy,

      # Connect status/control signals
      a_mux_sel = s.dpath.a_mux_sel,
      a_reg_en  = s.dpath.a_reg_en,
      b_mux_sel = s.dpath.b_mux_sel,
      b_reg_en  = s.dpath.b_reg_en,

      # Status signals (dpath -> ctrl)

      is_b_zero = s.dpath.is_b_zero,
      is_a_lt_b = s.dpath.is_a_lt_b,
    )

  # Line tracing

  def line_trace( s ):

    state_str = "? "
    if s.ctrl.state == s.ctrl.STATE_IDLE:
      state_str = "I "
    if s.ctrl.state == s.ctrl.STATE_CALC:
      if s.ctrl.do_swap:
        state_str = "Cs"
      elif s.ctrl.do_sub:
        state_str = "C-"
      else:
        state_str = "C "
    if s.ctrl.state == s.ctrl.STATE_DONE:
      state_str = "D "

    return f"{s.minion.req}({s.dpath.a_reg.line_trace()} " \
           f"{s.dpath.b_reg.line_trace()} {state_str}){s.minion.resp}"
