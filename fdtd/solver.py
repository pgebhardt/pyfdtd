import math
import numpy
import scipy.weave
from constants import constants
from material import material
from boundary import PML
import field as fi

class solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, field, mode='TMz', ports=None):
        # save arguments
        self.field = field
        self.mode = mode
        self.ports = ports
        self.material = material(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode, borderThickness=20.0)
        self.pml = PML(field.xSize, field.ySize, field.deltaX, field.deltaY, thickness=20.0)

    def iterate(self, duration, starttime=0.0, deltaT=0.0, safeHistory=False, historyInterval=0.0):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # calc deltaT
        if deltaT == 0.0:
            deltaT = 1.0/(constants.c0*math.sqrt(1.0/self.field.deltaX**2 + 1.0/self.field.deltaY**2))

        # create history memory
        history = []
        if safeHistory and historyInterval == 0.0:
            historyInterval = deltaT

        # create constants
        kx = deltaT/self.field.deltaX
        ky = deltaT/self.field.deltaY
        S = constants.c0*deltaT/math.sqrt(self.field.deltaX**2 + self.field.deltaY**2)

        if self.mode == 'TEz':
            kx, ky, = -ky, -ky

        # iterate
        for t in numpy.arange(starttime, starttime + duration, deltaT):
            # calc oddField
            self.field.oddFieldX['flux'][1:,1:] += ky*(self.field.evenFieldY['field'][1:,1:] - self.field.evenFieldY['field'][:-1,1:])
            self.field.oddFieldY['flux'][1:,1:] -= ky*(self.field.evenFieldX['field'][1:,1:] - self.field.evenFieldX['field'][1:,:-1])
             
            # calc field
            self.material.apply_odd(self.field, deltaT)

            # apply PML
            self.pml.apply_odd(self.field, deltaT)

            # update ports
            for port in self.ports:
                port.update(self.field, deltaT, S, t)

            # calc even Field
            self.field.evenFieldX['flux'][:,:-1] -= ky*(self.field.oddFieldX['field'][:,1:] + self.field.oddFieldY['field'][:,1:] - self.field.oddFieldX['field'][:,:-1] - self.field.oddFieldY['field'][:,:-1])
            self.field.evenFieldY['flux'][:-1,:] += kx*(self.field.oddFieldX['field'][1:,:] + self.field.oddFieldY['field'][1:,:] - self.field.oddFieldX['field'][:-1,:] - self.field.oddFieldY['field'][:-1,:])

            # calc field
            self.material.apply_even(self.field, deltaT)

            # apply PML
            self.pml.apply_even(self.field, deltaT)

            # safe Field
            if safeHistory and t/deltaT % (historyInterval/deltaT) < 1.0:
                history.append(self.field.oddFieldX['field'] + self.field.oddFieldY['field'])

            # print progression
            if t/deltaT % 100 < 1.0:
                print '{}%'.format((t-starttime)*100/duration)

        # return history
        return history
