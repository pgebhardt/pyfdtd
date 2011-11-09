import numpy
from constants import constants
import field as fi

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY, borderThickness=8.0, mode='TMz'):
        # init layer
        xShape = xSize/deltaX
        yShape = ySize/deltaY
        self.material = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape)) }

        # create memoryField
        self.memoryField = fi.field(xSize, ySize, deltaX, deltaY)

        # create mask
        self.mask = numpy.ones((xShape, yShape))
        for i in range(0, int(xShape), 1):
            for j in range(0, int(yShape), 1):
                if i <= borderThickness or j <= borderThickness or i >= xShape - borderThickness - 1 or j >= yShape - borderThickness - 1:
                    self.mask[i, j] = 0.0

        # save atributes
        self.mode = mode

    def empty_layer(self):
        """Returns an empty layer to work on"""
        return self.material.copy()

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

        field.oddFieldX['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.oddFieldX['flux'] - self.memoryField.oddFieldX['flux'])*self.mask + (1.0-self.mask)*field.oddFieldX['field']
        field.oddFieldY['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.oddFieldY['flux'] - self.memoryField.oddFieldY['flux'])*self.mask + (1.0-self.mask)*field.oddFieldY['field']

        self.memoryField.oddFieldX['flux'] += m2*field.oddFieldX['field']*deltaT*self.mask
        self.memoryField.oddFieldY['flux'] += m2*field.oddFieldY['field']*deltaT*self.mask

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

        field.evenFieldX['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux'])*self.mask + (1.0-self.mask)*field.evenFieldX['field']
        field.evenFieldY['field'] = (1.0/(c1*m1 + m2*deltaT))*(field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux'])*self.mask + (1.0-self.mask)*field.evenFieldY['field']

        self.memoryField.evenFieldX['flux'] += m2*field.evenFieldX['field']*deltaT*self.mask
        self.memoryField.evenFieldY['flux'] += m2*field.evenFieldY['field']*deltaT*self.mask
