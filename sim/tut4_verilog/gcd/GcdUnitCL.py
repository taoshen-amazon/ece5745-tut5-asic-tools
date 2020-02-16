#=========================================================================
# GCD Unit CL Model
#=========================================================================

from pymtl3      import *
from pymtl3.stdlib.cl import PipeQueueCL
from pymtl3.stdlib.ifcs import MinionIfcCL

from .GcdUnitMsg import GcdUnitMsgs

#-------------------------------------------------------------------------
# gcd
#-------------------------------------------------------------------------
# Helper function that uses Euclid's algorithm to calculate the greatest
# common denomiator, but also to estimate the number of cycles a simple
# FSM-based GCD unit might take.

def gcd_cl( a, b ):
  ncycles = 0
  while True:
    ncycles += 1
    if a < b:
      a,b = b,a
    elif b != 0:
      a = a - b
    else:
      return (a,ncycles)

#-------------------------------------------------------------------------
# GcdUnitCL
#-------------------------------------------------------------------------

class GcdUnitCL( Component ):

  # Constructor

  def construct( s ):

    # Interface

    s.minion = MinionIfcCL( GcdUnitMsgs.req, GcdUnitMsgs.resp )

    # Adapters

    s.req_q  = PipeQueueCL(1)( enq = s.minion.req )

    # Member variables

    s.result  = None
    s.counter = 0

    # Concurrent block

    @s.update
    def block():

      if s.result is not None:
        # Handle delay to model the gcd unit latency
        if s.counter > 0:
          s.counter -= 1
        elif s.minion.resp.rdy():
          s.minion.resp( s.result )
          s.result = None

      elif s.req_q.deq.rdy():
        msg = s.req_q.deq()
        s.result, s.counter = gcd_cl(msg.a, msg.b)

  # Line tracing

  def line_trace( s ):
    return f"{s.minion.req}({s.counter:^4}){s.minion.resp}"
