import numpy
import math
import copy
import field as fi
from material import material
from constants import constants

class pml:
    """Applies a perfectly matched layer as surounding boundary conditions"""
    def __init__(self, xSize, ySize, deltaX, deltaY, thickness=20.0, mode='TMz'):
        # init layer container
        self.layer = {}

        # crate material
        xShape, yShape = xSize/deltaX, ySize/deltaY
        sigma = { 'electricX': numpy.zeros((xShape, yShape)), 'electricY': numpy.zeros((xShape, yShape)), 'magneticX': numpy.zeros((xShape, yShape)), 'magneticY': numpy.zeros((xShape, yShape)) }
        mask = numpy.zeros((xShape, yShape))

        # set constant
        c1 = constants.mu0/constants.e0

        # init PML
        sigmaMax = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-15)/(2.0*deltaX*thickness)

        for n in range(0, int(thickness+1.0), 1):
            for j in range(0, int(yShape), 1):
                sigma['electricY'][n, j] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
                sigma['magneticY'][n, j] = sigmaMax*math.pow(float(thickness-n-0.5)/thickness, 3.0)*c1
                mask[n, j] = 1.0

                sigma['electricY'][xShape-1-n, j] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
                sigma['magneticY'][xShape-1-n, j] = sigmaMax*math.pow(float(thickness-n+0.5)/thickness, 3.0)*c1
                mask[xShape-1-n, j] = 1.0

            for i in range(0, int(xShape), 1):
                sigma['electricX'][i, n] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
                sigma['magneticX'][i, n] = sigmaMax*math.pow(float(thickness-n-0.5)/thickness, 3.0)*c1
                mask[i, n] = 1.0

                sigma['electricX'][i, yShape-1-n] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
                sigma['magneticX'][i, yShape-1-n] = sigmaMax*math.pow(float(thickness-n+0.5)/thickness, 3.0)*c1
                mask[i, yShape-1-n] = 1.0

        # create layer
        if mode == 'TMz':
            self.layer['electric'] = (copy.deepcopy(material.epsilon(1.0, sigma['electricX'])), copy.deepcopy(material.epsilon(1.0, sigma['electricY'])), mask)
            self.layer['magnetic'] = (copy.deepcopy(material.mu(1.0, sigma['magneticX'])), copy.deepcopy(material.mu(1.0, sigma['magneticY'])), mask)
        elif mode == 'TEz':
            self.layer['magnetic'] = (copy.deepcopy(material.mu(1.0, sigma['magneticX'])), copy.deepcopy(material.mu(1.0, sigma['magneticY'])), mask)
            self.layer['electric'] = (copy.deepcopy(material.epsilon(1.0, sigma['electricX'])), copy.deepcopy(material.epsilon(1.0, sigma['electricY'])), mask)
