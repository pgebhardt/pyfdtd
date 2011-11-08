import numpy
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
        self.material = material(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode)
        self.pml = PML(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode)

    def iterate(self, deltaT, time, starttime=0.0):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/self.field.deltaX
        c2 = deltaT/self.field.deltaY
        c3 = constants.permit
        c4 = constants.permea

        if self.mode == 'TEz':
            c1, c2, c3, c4 = -c1, -c2, c4, c3

        # iterate
        for t in numpy.arange(starttime, starttime + time, deltaT):
            # update ports
            for port in self.ports:
                port.update(self.field, t)

            # calc odd Field
            xshape, yshape = self.field.oddFieldX['field'].shape
            for x in range(1, xshape, 1):
                for y in range(1, yshape, 1):
                    # calc flux density
                    self.field.oddFieldX['flux'][x, y] += c1*(self.field.evenFieldY['field'][x, y] - self.field.evenFieldY['field'][x-1, y]) 
                    self.field.oddFieldY['flux'][x, y] -= c2*(self.field.evenFieldX['field'][x, y] - self.field.evenFieldX['field'][x, y-1])
                    
            # calc field
            self.material.apply_odd(self.field, deltaT)

            # apply PML
            self.pml.apply_odd(self.field, deltaT)

            # calc even Field
            for x in range(0, xshape, 1):
                for y in range(0, yshape-1, 1):
                    # calc flux density
                    self.field.evenFieldX['flux'][x, y] -= c2*(self.field.oddFieldX['field'][x, y+1] + self.field.oddFieldY['field'][x, y+1] - self.field.oddFieldX['field'][x, y] - self.field.oddFieldY['field'][x, y])

            for x in range(0, xshape-1, 1):
                for y in range(0, yshape, 1):
                    # calc flux density
                    self.field.evenFieldY['flux'][x, y] += c1*(self.field.oddFieldX['field'][x+1, y] + self.field.oddFieldY['field'][x+1, y] - self.field.oddFieldX['field'][x, y] - self.field.oddFieldY['field'][x, y])

            # calc field
            self.material.apply_even(self.field, deltaT)

            # apply PML
            self.pml.apply_even(self.field, deltaT)

            if t/deltaT % 100 == 0:
                print "{}%".format((t-starttime)*100/time)
