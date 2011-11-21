import math
import numpy
from constants import constants
from material import material
from pml import pml
import field as fi

class solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, field, mode='TMz', ports=[], boundary=None):
        # save arguments
        self.field = field
        self.mode = mode
        self.ports = ports

        # create free space material
        self.material = material(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode)

        # create standart boundary
        self.boundary = pml(field.xSize, field.ySize, field.deltaX, field.deltaY, thickness=20.0)

    def solve(self, duration, starttime=0.0, deltaT=0.0, saveHistory=False, maxHistoryMemory=256e6):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # calc deltaT
        if deltaT == 0.0:
            deltaT = 1.0/(constants.c0*math.sqrt(1.0/self.field.deltaX**2 + 1.0/self.field.deltaY**2))

        # create history memory
        history = []
        if saveHistory:
            xShape, yShape = self.field.oddFieldX['flux'].shape
            historyInterval = xShape*yShape*duration/(maxHistoryMemory/4.0)

        # create constants
        kx = deltaT/self.field.deltaX
        ky = deltaT/self.field.deltaY
        S = constants.c0*deltaT/math.sqrt(self.field.deltaX**2 + self.field.deltaY**2)

        # apply mode
        if self.mode == 'TEz':
            kx, ky = -ky, -ky

        # iterate
        for t in numpy.arange(starttime, starttime + duration, deltaT):
            # do step
            self._step(deltaT, t, kx, ky)

            #safe History
            if saveHistory and t/deltaT % (historyInterval/deltaT) < 1.0:
                history.append(self.field.oddFieldX['field'] + self.field.oddFieldY['field'])

            # print progession
            if t/deltaT % 100 < 1.0:
                print '{}%'.format((t-starttime)*100/duration)

        # return history
        return history

    def _step(self, deltaT, t, kx, ky):
        # calc oddField
        self.field.oddFieldX['flux'][1:,1:] += kx*(self.field.evenFieldY['field'][1:,1:] - self.field.evenFieldY['field'][:-1,1:])
        self.field.oddFieldY['flux'][1:,1:] -= ky*(self.field.evenFieldX['field'][1:,1:] - self.field.evenFieldX['field'][1:,:-1])
         
        # apply material and PML
        self.material.apply_odd(self.field, deltaT)
        self.boundary.apply_odd(self.field, deltaT)

        # update ports
        for port in self.ports:
            port.update(self.field, t)

        # calc evenField
        self.field.evenFieldX['flux'][:,:-1] -= ky*(self.field.oddFieldX['field'][:,1:] + self.field.oddFieldY['field'][:,1:] - self.field.oddFieldX['field'][:,:-1] - self.field.oddFieldY['field'][:,:-1])
        self.field.evenFieldY['flux'][:-1,:] += kx*(self.field.oddFieldX['field'][1:,:] + self.field.oddFieldY['field'][1:,:] - self.field.oddFieldX['field'][:-1,:] - self.field.oddFieldY['field'][:-1,:])

        # apply material and PML
        self.material.apply_even(self.field, deltaT)
        self.boundary.apply_even(self.field, deltaT)
