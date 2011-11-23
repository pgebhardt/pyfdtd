import numpy
import math
import copy
import field as fi
from material import material
from constants import constants

class pml:
    """Applies a perfectly matched layer as surounding boundary conditions"""
    def __init__(self, mat, thickness, mode='TMz'):
        # set constant
        c = constants.mu0/constants.e0

        # init PML
        sigma = -(3.0 + 1.0)*constants.e0*constants.c0*math.log(1.0e-15)/(2.0*deltaX*thickness)

        # create layer
        mat['electric'][:,:thickness] = material.epsilon(sigma=sigma)
        mat['magnetic'][:,:thickness] = material.mu(sigma=sigma*c)
        mat['electric'][:,-thickness:] = material.epsilon(sigma=sigma)
        mat['magnetic'][:,-thickness:] = material.mu(sigma=sigma*c)
        mat['electric'][:thicknessm:] = material.epsilon(sigma=sigma)
        mat['magnetic'][:thickness,:] = material.mu(sigma=sigma*c)
        mat['electric'][-thickness:,:] = material.epsilon(sigma=sigma)
        mat['magnetic'][-thickness:,:] = material.mu(sigma=sigma*c)
