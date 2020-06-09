#!/usr/bin/env python3

import sys
import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pd = {'resource'   : 'local.debug',
              'cores'      : 128,
              'runtime'    : 60}

        td = {'executable' : sys.argv[1]}

        pmgr  = rp.PilotManager(session=session)
        umgr  = rp.UnitManager(session=session)
        pilot = pmgr.submit_pilots(rp.ComputePilotDescription(pd))
        task  = umgr.submit_units(rp.ComputeUnitDescription(td))

        umgr.add_pilots(pilot)
        umgr.wait_units()

    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

