import numpy
import math
import field as fi
from constants import constants

class PML:
    """Handles borders"""
    def __init__(self, xSize, ySize, deltaX, deltaY, thickness=8.0, mode='TMz'):
        # init
        self.mode = mode
        self.memoryField = fi.field(xSize, ySize, deltaX, deltaY)

        # crate material
        xShape, yShape = xSize/deltaX, ySize/deltaY
        self.material = { 'sigmaOddX': numpy.zeros((xShape, yShape)), 'sigmaOddY': numpy.zeros((xShape, yShape)), 'sigmaEvenX': numpy.zeros((xShape, yShape)), 'sigmaEvenY': numpy.zeros((xShape, yShape)) }
        self.mask = numpy.zeros((xShape, yShape))

        # apply mode
        c1, c2 = 1.0, constants.u0/constants.e0
        if mode == 'TEz':
            c1, c2 = c2, c1

        # init PML
        sigmaMaxX = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-8)/(2.0*deltaX*thickness)
        sigmaMaxY = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-8)/(2.0*deltaY*thickness)
        print sigmaMaxX*c1, sigmaMaxX*c2

        for n in range(0, int(thickness+1.0), 1):
            for j in range(0, int(yShape), 1):
                self.material['sigmaOddX'][n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenX'][n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c2
                self.mask[n, j] = 1.0

                self.material['sigmaOddX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c2
                self.mask[xShape-1-n, j] = 1.0

            for i in range(0, int(xShape), 1):
                self.material['sigmaOddY'][i, n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenY'][i, n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c2
                self.mask[i, n] = 1.0

                self.material['sigmaOddY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                self.material['sigmaEvenY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c2
                self.mask[i, yShape-1-n] = 1.0

    def apply_odd(self, field, deltaT):
        # calc oddGrid
        c1 = constants.e0
        if self.mode == 'TEz':
            c1 = constants.u0

        field.oddFieldX['field'] = (1.0/(c1 + self.material['sigmaOddX']*deltaT))*(field.oddFieldX['flux'] - self.memoryField.oddFieldX['flux'])*self.mask + (1.0-self.mask)*field.oddFieldX['field']
        field.oddFieldY['field'] = (1.0/(c1 + self.material['sigmaOddY']*deltaT))*(field.oddFieldY['flux'] - self.memoryField.oddFieldY['flux'])*self.mask + (1.0-self.mask)*field.oddFieldY['field']

        self.memoryField.oddFieldX['flux'] += self.material['sigmaOddX']*field.oddFieldX['field']*deltaT*self.mask
        self.memoryField.oddFieldY['flux'] += self.material['sigmaOddY']*field.oddFieldY['field']*deltaT*self.mask

        # apply boundary condition
        field.oddFieldX['field'][:1,:] = 0.0
        field.oddFieldY['field'][:1,:] = 0.0
        field.oddFieldX['field'][-1:,:] = 0.0
        field.oddFieldY['field'][-1:,:] = 0.0
        
        field.oddFieldX['field'][:,:1] = 0.0
        field.oddFieldY['field'][:,:1] = 0.0
        field.oddFieldX['field'][:,-1:] = 0.0
        field.oddFieldY['field'][:,-1:] = 0.0

    def apply_even(self, field, deltaT):
        # calc oddGrid
        c1 = constants.u0
        if self.mode == 'TEz':
            c1 = constants.e0

        field.evenFieldX['field'] = (1.0/(c1 + self.material['sigmaEvenX']*deltaT))*(field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux'])*self.mask + (1.0-self.mask)*field.evenFieldX['field']
        field.evenFieldY['field'] = (1.0/(c1 + self.material['sigmaEvenY']*deltaT))*(field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux'])*self.mask + (1.0-self.mask)*field.evenFieldY['field']

        self.memoryField.evenFieldX['flux'] += self.material['sigmaEvenX']*field.evenFieldX['field']*deltaT*self.mask
        self.memoryField.evenFieldY['flux'] += self.material['sigmaEvenY']*field.evenFieldY['field']*deltaT*self.mask
        
