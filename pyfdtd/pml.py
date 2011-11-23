import numpy
import math
import field as fi
from material import material
from constants import constants

class pml:
    """Applies a perfectly matched layer as surounding boundary conditions"""
    def __init__(self, xSize, ySize, deltaX, deltaY, thickness=8.0):
        # init layer container
        self.layer = {}

        # crate material
        xShape, yShape = xSize/deltaX, ySize/deltaY
        sigma = { 'electricX': numpy.zeros((xShape, yShape)), 'electricY': numpy.zeros((xShape, yShape)), 'magneticX': numpy.zeros((xShape, yShape)), 'magneticY': numpy.zeros((xShape, yShape)) }
        mask = numpy.zeros((xShape, yShape))

        # set constant
        c1 = constants.mu0/constants.e0

        # init PML
        sigmaMaxX = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-8)/(2.0*deltaX*thickness)
        sigmaMaxY = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-8)/(2.0*deltaY*thickness)

        for n in range(0, int(thickness+1.0), 1):
            for j in range(0, int(yShape), 1):
                sigma['electricX'][n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)
                sigma['magneticX'][n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                mask[n, j] = 1.0

                sigma['electricX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)
                sigma['magneticX'][xShape-1-n, j] = sigmaMaxY*math.pow((thickness-n)/thickness, 3.0)*c1
                mask[xShape-1-n, j] = 1.0

            for i in range(0, int(xShape), 1):
                sigma['electricY'][i, n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)
                sigma['magneticY'][i, n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                mask[i, n] = 1.0

                sigma['electricY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)
                sigma['magneticY'][i, yShape-1-n] = sigmaMaxX*math.pow((thickness-n)/thickness, 3.0)*c1
                mask[i, yShape-1-n] = 1.0

    def apply_odd(self, field, deltaT):
        """applies pml for odd field components"""
        # calc oddGrid
        c1 = constants.e0
        if self.mode == 'TEz':
            c1 = constants.mu0

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
        """applies pml for even field components"""
        # calc oddGrid
        c1 = constants.mu0
        if self.mode == 'TEz':
            c1 = constants.e0

        field.evenFieldX['field'] = (1.0/(c1 + self.material['sigmaEvenX']*deltaT))*(field.evenFieldX['flux'] - self.memoryField.evenFieldX['flux'])*self.mask + (1.0-self.mask)*field.evenFieldX['field']
        field.evenFieldY['field'] = (1.0/(c1 + self.material['sigmaEvenY']*deltaT))*(field.evenFieldY['flux'] - self.memoryField.evenFieldY['flux'])*self.mask + (1.0-self.mask)*field.evenFieldY['field']

        self.memoryField.evenFieldX['flux'] += self.material['sigmaEvenX']*field.evenFieldX['field']*deltaT*self.mask
        self.memoryField.evenFieldY['flux'] += self.material['sigmaEvenY']*field.evenFieldY['field']*deltaT*self.mask
        
