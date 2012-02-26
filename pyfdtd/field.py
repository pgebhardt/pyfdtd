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


class Field:
    """
    Defines the calculation domain by creating even and odd yee grids
    for field and flux.

        **Arguments:**

    size (required)
        Size of domain

    delta (required)
        Discretisation of domain

    """
    def __init__(self, size, delta):
        # get values
        sizeX, sizeY = size
        deltaX, deltaY = delta

        # create even and odd Field
        self.evenFieldX = {
                'field': numpy.zeros((sizeX / deltaX, sizeY / deltaY)),
                'flux': numpy.zeros((sizeX / deltaX, sizeY / deltaY))}
        self.evenFieldY = {
                'field': numpy.zeros((sizeX / deltaX, sizeY / deltaY)),
                'flux': numpy.zeros((sizeX / deltaX, sizeY / deltaY))}
        self.oddFieldX = {
                'field': numpy.zeros((sizeX / deltaX, sizeY / deltaY)),
                'flux': numpy.zeros((sizeX / deltaX, sizeY / deltaY))}
        self.oddFieldY = {
                'field': numpy.zeros((sizeX / deltaX, sizeY / deltaY)),
                'flux': numpy.zeros((sizeX / deltaX, sizeY / deltaY))}

        # save all given information
        self.size = size
        self.delta = delta

    def __getitem__(self, key):
        """Returns the field vector at the given location"""
        # obtain parameter
        x, y = key
        deltaX, deltaY = self.delta

        # scale x, y
        x, y = int(x / deltaX), int(y / deltaY)

        # return field vector
        return (self.evenFieldX['field'][x, y], self.evenFieldY['field'][x, y],
                self.oddFieldX['field'][x, y] + self.oddFieldY['field'][x, y])
