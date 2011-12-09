import numpy
import math
import copy
import field as fi
from material import material
from constants import constants


def pml(xSize, ySize, deltaX, deltaY, thickness=20.0, mode='TMz'):
    """creates a perfectly matched layer as surounding boundary conditions"""
    # crate material
    xShape, yShape = xSize/deltaX, ySize/deltaY
    sigma = { 'electricX': numpy.zeros((xShape, yShape)), 'electricY': numpy.zeros((xShape, yShape)), 'magneticX': numpy.zeros((xShape, yShape)), 'magneticY': numpy.zeros((xShape, yShape)) }
    mask = numpy.zeros((xShape, yShape))

    # set constant
    c = constants.mu0/constants.e0

    # init PML
    sigmaMax = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-5)/(2.0*deltaX*thickness)

    for n in range(0, int(thickness+1.0), 1):
        for j in range(0, int(yShape), 1):
            sigma['electricY'][n, j] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
            sigma['magneticY'][n, j] = sigmaMax*math.pow(float(thickness-n-0.5)/thickness, 3.0)*c
            mask[n, j] = 1.0

            sigma['electricY'][xShape-1-n, j] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
            sigma['magneticY'][xShape-1-n, j] = sigmaMax*math.pow(float(thickness-n+0.5)/thickness, 3.0)*c
            mask[xShape-1-n, j] = 1.0

        for i in range(0, int(xShape), 1):
            sigma['electricX'][i, n] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
            sigma['magneticX'][i, n] = sigmaMax*math.pow(float(thickness-n-0.5)/thickness, 3.0)*c
            mask[i, n] = 1.0

            sigma['electricX'][i, yShape-1-n] = sigmaMax*math.pow(float(thickness-n)/thickness, 3.0)
            sigma['magneticX'][i, yShape-1-n] = sigmaMax*math.pow(float(thickness-n+0.5)/thickness, 3.0)*c
            mask[i, yShape-1-n] = 1.0

    # create layer
    electric = material.epsilon(1.0, sigma['electricX']), material.epsilon(1.0, sigma['electricY'])
    magnetic = material.mu(1.0, sigma['magneticX']), material.mu(1.0, sigma['magneticY'])
    return electric, magnetic, mask
