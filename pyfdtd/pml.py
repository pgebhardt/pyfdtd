# pyfdtd is a simple 2d fdtd using numpy
# Copyright (C) 2012  Patrik Gebhardt
# Contact: grosser.knuff@googlemail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy
import math
import pyopencl.array as clarray
from material import Material
from scipy import constants


def pml(queue, size, delta, thickness=20.0, mode='TMz'):
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
    c = constants.mu_0 / constants.epsilon_0

    # init PML
    sigmaMax = -(3.0 + 1.0) * constants.epsilon_0 * constants.c \
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
    electric = (
        Material.epsilon(1.0, clarray.to_device(queue, sigma['electricX'])),
        Material.epsilon(1.0, clarray.to_device(queue, sigma['electricY'])))
    magnetic = (
        Material.mu(1.0, clarray.to_device(queue, sigma['magneticX'])),
        Material.mu(1.0, clarray.to_device(queue, sigma['magneticY'])))

    return electric, magnetic, mask
