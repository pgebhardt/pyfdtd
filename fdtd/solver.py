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
        self.material = material(field.xSize, field.ySize, field.deltaX, field.deltaY)
        self.pml = PML(field.xSize, field.ySize, field.deltaX, field.deltaY, mode=self.mode)

        # create memory field
        self.memoryField = fi.field(self.field.xSize, self.field.ySize, self.field.deltaX, self.field.deltaY)

    def iterate(self, deltaT, time, starttime=0.0):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/self.field.deltaX
        c2 = deltaT/self.field.deltaY
        c3 = constants.permit
        c4 = constants.permea

        # shortcut materials
        mat = self.material.get_material()
        m1 = mat['epsilon']
        m2 = mat['mu']
        m3 = mat['sigma']
        m4 = numpy.zeros(mat['sigma'].shape)

        if self.mode == 'TEz':
            c1, c2, c3, c4 = -c1, -c2, c4, c3
            m1, m2, m3, m4 = m2, m1, m4, m3

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
            self.field.oddFieldX['field'] = (1.0/(c3*m1 + m3))*(self.field.oddFieldX['flux'] - self.memoryField.oddFieldX['flux']*deltaT)
            self.field.oddFieldY['field'] = (1.0/(c3*m1 + m3))*(self.field.oddFieldY['flux'] - self.memoryField.oddFieldY['flux']*deltaT)
            # integrate field
            self.memoryField.oddFieldX['flux'] += m3*self.field.oddFieldX['field']*deltaT
            self.memoryField.oddFieldY['flux'] += m3*self.field.oddFieldY['field']*deltaT

            # apply PML
            self.pml.apply_odd(self.field, deltaT)

            # calc even Field
            for x in range(0, xshape, 1):
                for y in range(0, yshape-1, 1):
                    # calc flux density
                    self.field.evenFieldX['flux'][x, y] -= c2*(self.field.oddFieldX['field'][x, y+1] + self.field.oddFieldY['field'][x, y+1] - self.field.oddFieldX['field'][x, y] - self.field.oddFieldY['field'][x, y])

            # calc field
            self.field.evenFieldX['field'] = (1.0/(c4*m2 + m4))*(self.field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux']*deltaT)
            # integrate field
            self.memoryField.evenFieldX['flux'] += m4*self.field.evenFieldX['field']*deltaT

            for x in range(0, xshape-1, 1):
                for y in range(0, yshape, 1):
                    # calc flux density
                    self.field.evenFieldY['flux'][x, y] += c1*(self.field.oddFieldX['field'][x+1, y] + self.field.oddFieldY['field'][x+1, y] - self.field.oddFieldX['field'][x, y] - self.field.oddFieldY['field'][x, y])

            # calc field
            self.field.evenFieldY['field'] = (1.0/(c4*m2 + m4))*(self.field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux']*deltaT)
            # integrate field
            self.memoryField.evenFieldY['flux'] += m4*self.field.evenFieldY['field']*deltaT

            # apply PML
            self.pml.apply_even(self.field, deltaT)

            if t/deltaT % 100 == 0:
                print "{}%".format((t-starttime)*100/time)
