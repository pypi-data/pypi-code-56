from .sprim import SPrim

import numpy as np
import pyopencl as cl
import pyopencl.array as clarr

import os
import re

class SFermiChop(SPrim):
    """
    Scattering kernel for Fermi chopper component. Replicates the functionality of the
    FermiChopper component in McStas. 

    Parameters
    ----------

    Methods
    -------
    Data
        None
    Plot
        None
    Save
        None

    """

    def __init__(self, radius, nslit, length, width, 
                 nu, phase=0.0, eff=1.0, curvature=0.0, R0=0, Qc=0, 
                 alpha=0, m=1, W=0, idx=0, ctx=0, **kwargs):
        self.radius = np.float32(radius)
        self.nslit = np.uint32(nslit)
        self.length = np.float32(length)
        self.width = np.float32(width)
        self.nu = np.float32(nu)
        self.phase = np.float32(phase)
        self.eff = np.float32(eff)
        self.curvature = np.float32(curvature)
        self.R0     = np.float32(R0)
        self.Qc     = np.float32(Qc)
        self.alpha  = np.float32(alpha)
        self.m      = np.float32(m)
        self.W      = np.float32(W)
        self.idx = np.uint32(idx)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fermichop.cl'), mode='r') as f:
            self.prg = cl.Program(ctx, f.read()).build(options=r'-I "{}/include"'.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    def scatter_prg(self, queue, N, neutron_buf, intersection_buf, iidx_buf):
        self.prg.fermichop(queue, (N, ),
                                None,
                                neutron_buf,
                                intersection_buf,
                                iidx_buf,
                                self.radius,
                                self.nslit,
                                self.length,
                                self.width,
                                self.phase,
                                self.nu,
                                self.eff,
                                self.curvature,
                                self.m,
                                self.alpha,
                                self.Qc,
                                self.W,
                                self.R0,
                                self.idx)