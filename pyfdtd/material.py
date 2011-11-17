from types import *
import numpy
from constants import constants
import field as fi

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY, mode='TMz'):
        # init layer
        xShape = xSize/deltaX
        yShape = ySize/deltaY
        self.material = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape)) }

        # create memoryField
        self.memoryField = fi.field(xSize, ySize, deltaX, deltaY)

        # save atributes
        self.mode = mode
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize

    def __getitem__(self, key):
        """Return material at given location"""
        # obtain parametes
        mat, x, y = key

        # scale slices
        if x.start:
            x = slice(int(x.start/self.deltaX), x.stop)
        if x.stop:
            x = slice(x.start, int(x.stop/self.deltaX))
        if y.start:
            y = slice(int(y.start/self.deltaY), y.stop)
        if y.stop:
            y = slice(y.start, int(y.stop/self.deltaY))

        # return material
        return self.material[mat][x, y]

    def __setitem__(self, key, value):
        """Set material either at given location or using a function"""
        # A function value is obtained
        if isinstance(value, FunctionType):
            for x in numpy.arange(0.0, self.xSize, self.deltaX):
                for y in numpy.arange(0.0, self.ySize, self.deltaY):
                    self.material[key][int(x/self.deltaX), int(y/self.deltaY)] = value(x, y)

        else:
            # A value type is obtained
            mat, x, y = key

            # scale slices
            if x.start:
                x = slice(int(x.start/self.deltaX), x.stop)
            if x.stop:
                x = slice(x.start, int(x.stop/self.deltaX))
            if y.start:
                y = slice(int(y.start/self.deltaY), y.stop)
            if y.stop:
                y = slice(y.start, int(y.stop/self.deltaY))

            # set material
            self.material[mat][x, y] = value

    def apply_odd(self, field, deltaT):
        """Calculate field for oddField"""
        # switch mode
        c1 = constants.e0
        m1 = self.material['epsilon']
        m2 = self.material['sigma']

        if self.mode == 'TEz':
            c1 = constants.u0
            m1 = self.material['mu']
            m2 = numpy.zeros(self.material['sigma'].shape)

        field.oddFieldX['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.oddFieldX['flux'] - self.memoryField.oddFieldX['flux'])
        field.oddFieldY['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.oddFieldY['flux'] - self.memoryField.oddFieldY['flux'])

    def apply_even(self, field, deltaT):
        """Calculate field for evenField"""
        # switch mode
        c1 = constants.u0
        m1 = self.material['mu']
        m2 = numpy.zeros(self.material['sigma'].shape)

        if self.mode == 'TEz':
            c1 = constants.e0
            m1 = self.material['epsilon']
            m2 = self.material['sigma']

        field.evenFieldX['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux'])
        field.evenFieldY['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux'])
