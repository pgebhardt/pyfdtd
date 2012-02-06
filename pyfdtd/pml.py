import numpy
import math
from material import material
from constants import constants


def pml(size, delta, thickness=20.0, mode='TMz'):
    """creates a perfectly matched layer as surounding boundary conditions"""
    # get patameter
    sizeX, sizeY = size
    deltaX, deltaY = delta

    # crate material
    shapeX, shapeY = sizeX / deltaX, sizeY / deltaY
    sigma = {
            'electricX': numpy.zeros((shapeX, shapeY)),
            'electricY': numpy.zeros((shapeX, shapeY)),
            'magneticX': numpy.zeros((shapeX, shapeY)),
            'magneticY': numpy.zeros((shapeX, shapeY))}
    mask = numpy.zeros((shapeX, shapeY))

    # set constant
    c = constants.mu0 / constants.e0

    # init PML
    sigmaMax = -(3.0 + 1.0) * constants.e0 * constants.c0 \
            * math.log(1.0e-5) / (2.0 * deltaX * thickness)

    for n in range(0, int(thickness + 1.0), 1):
        for j in range(0, int(shapeY), 1):
            sigma['electricY'][n, j] = sigmaMax \
                    * math.pow(float(thickness - n) / thickness, 3.0)
            sigma['magneticY'][n, j] = sigmaMax \
                    * math.pow(float(thickness - n - 0.5) / thickness, 3.0) * c
            mask[n, j] = 1.0

            sigma['electricY'][shapeX - 1 - n, j] = sigmaMax \
                    * math.pow(float(thickness - n) / thickness, 3.0)
            sigma['magneticY'][shapeX - 1 - n, j] = sigmaMax \
                    * math.pow(float(thickness - n + 0.5) / thickness, 3.0) * c
            mask[shapeX - 1 - n, j] = 1.0

        for i in range(0, int(shapeX), 1):
            sigma['electricX'][i, n] = sigmaMax \
                    * math.pow(float(thickness - n) / thickness, 3.0)
            sigma['magneticX'][i, n] = sigmaMax \
                    * math.pow(float(thickness - n - 0.5) / thickness, 3.0) * c
            mask[i, n] = 1.0

            sigma['electricX'][i, shapeY - 1 - n] = sigmaMax \
                    * math.pow(float(thickness - n) / thickness, 3.0)
            sigma['magneticX'][i, shapeY - 1 - n] = sigmaMax \
                    * math.pow(float(thickness - n + 0.5) / thickness, 3.0) * c
            mask[i, shapeY - 1 - n] = 1.0

    # create layer
    electric = (material.epsilon(1.0, sigma['electricX']),
            material.epsilon(1.0, sigma['electricY']))
    magnetic = (material.mu(1.0, sigma['magneticX']),
            material.mu(1.0, sigma['magneticY']))

    return electric, magnetic, mask
