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

    def empty_layer(self):
        """Returns an empty layer to work on"""
        result = { 'epsilon': self.material['epsilon'].copy(), 'mu': self.material['mu'].copy(), 'sigma': self.material['sigma'].copy() }
        return result

    def add_layer(self, layer):
        """Add new layer to material"""
        #calc new material
        xShape, yShape = layer['epsilon'].shape
        for i in range(0, xShape, 1):
            for j in range(0, yShape, 1):
                # cumulate epsilon
                if layer['epsilon'][i, j] != 1.0:
                    self.material['epsilon'][i, j] = layer['epsilon'][i, j]

                #cumulate mu
                if layer['mu'][i, j] != 1.0:
                    self.material['mu'][i, j] = layer['mu'][i, j]

                #cumulate sigma
                if layer['sigma'][i, j] != 0.0:
                    self.material['sigma'][i, j] = layer['sigma'][i, j]

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
