import numpy
import math
import field as fi
from material import material
from constants import constants

class pml:
    """Applies a perfectly matched layer as surounding boundary conditions"""
    def __init__(self, xSize, ySize, deltaX, deltaY, thickness=8.0, mode='TMz'):
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

        # create odd field function
        def oddField(flux, dt):


        # apply boundary condition
        field.oddFieldX['field'][:1,:] = 0.0
        field.oddFieldY['field'][:1,:] = 0.0
        field.oddFieldX['field'][-1:,:] = 0.0
        field.oddFieldY['field'][-1:,:] = 0.0
        
        field.oddFieldX['field'][:,:1] = 0.0
        field.oddFieldY['field'][:,:1] = 0.0
        field.oddFieldX['field'][:,-1:] = 0.0
        field.oddFieldY['field'][:,-1:] = 0.0 
