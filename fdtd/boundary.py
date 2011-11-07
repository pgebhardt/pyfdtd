import numpy
import math
import field as fi
from constants import constants

class PML:
    """Handles borders"""
    def __init__(self, xSize, ySize, deltaX, deltaY, thickness=10.0, mode='TMz'):
        # init
        self.mode = mode
        self.memoryField = fi.field(xSize, ySize, deltaX, deltaY)

        # crate material
        xShape, yShape = xSize/deltaX, ySize/deltaY
        self.material = { 'sigmaOddX': numpy.zeros((xShape, yShape)), 'sigmaOddY': numpy.zeros((xShape, yShape)), 'sigmaEvenX': numpy.zeros((xShape, yShape)), 'sigmaEvenY': numpy.zeros((xShape, yShape)) }

        # apply mode
        c1, c2 = 1.0, constants.permea/constants.permit
        if mode == 'TEz':
            c1, c2 = c2, c1

        # init PML
        sigmaMaxX = -(3.0 + 1.0)*math.sqrt(constants.permit/constants.permea)*math.log(1.0e-8)/(2.0*deltaX*thickness)
        sigmaMaxY = -(3.0 + 1.0)*math.sqrt(constants.permit/constants.permea)*math.log(1.0e-8)/(2.0*deltaY*thickness)

        for n in range(0, int(thickness), 1):
            for j in range(0, int(yShape), 1):
                self.material['sigmaOddX'][n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenX'][n, j] = sigmaMaxY*math.pow((thickness-n+0.5)/thickness, 3.0)*c2

                self.material['sigmaOddX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n+0.5)/thickness, 3.0)*c2

            for i in range(0, int(xShape), 1):
                self.material['sigmaOddY'][i, n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenY'][i, n] = sigmaMaxX*math.pow((thickness-n+0.5)/thickness, 3.0)*c2

                self.material['sigmaOddY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n+0.5)/thickness, 3.0)*c2

    def apply_odd(self, field, deltaT):
        # calc oddGrid
        c1 = constants.permit
        if self.mode == 'TEz':
            c1 = constants.permea

        field.oddFieldX['field'] = (1.0/(c1 + self.material['sigmaOddX']*deltaT))*(field.oddFieldX['flux'] - self.memoryField.oddFieldX['flux'])
        field.oddFieldY['field'] = (1.0/(c1 + self.material['sigmaOddY']*deltaT))*(field.oddFieldY['flux'] - self.memoryField.oddFieldY['flux'])

        self.memoryField.oddFieldX['flux'] += self.material['sigmaOddX']*field.oddFieldX['field']*deltaT
        self.memoryField.oddFieldY['flux'] += self.material['sigmaOddY']*field.oddFieldY['field']*deltaT

        # apply boundary condition
        xShape, yShape = field.oddFieldX['field'].shape
        for i in range(0, yShape-1, 1):
            field.oddFieldX['field'][0, i] = 0.0
            field.oddFieldY['field'][0, i] = 0.0
            field.oddFieldX['field'][xShape-2, i] = 0.0
            field.oddFieldY['field'][xShape-2, i] = 0.0

        for i in range(0, xShape-1, 1):
            field.oddFieldX['field'][i, 0] = 0.0
            field.oddFieldY['field'][i, 0] = 0.0
            field.oddFieldX['field'][i, yShape-2] = 0.0
            field.oddFieldY['field'][i, yShape-2] = 0.0

    def apply_even(self, field, deltaT):
        # calc oddGrid
        c1 = constants.permea
        if self.mode == 'TEz':
            c1 = constants.permit

        field.evenFieldX['field'] = (1.0/(c1 + self.material['sigmaEvenX']*deltaT))*(field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux'])
        field.evenFieldY['field'] = (1.0/(c1 + self.material['sigmaEvenY']*deltaT))*(field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux'])

        self.memoryField.evenFieldX['flux'] += self.material['sigmaEvenX']*field.evenFieldX['field']*deltaT
        self.memoryField.evenFieldY['flux'] += self.material['sigmaEvenY']*field.evenFieldY['field']*deltaT
        
