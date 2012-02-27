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
import pyopencl.array as clarray


class Buffer:
    def __init__(self, queue, shape):
        # create numpy array
        self.narray = numpy.zeros(shape)

        # create cl array
        self.clarray = clarray.to_device(queue, self.narray)

    def to_cl(self, queue):
        # copy numpy to cl
        self.clarray = clarray.to_device(queue, self.narray)

    def to_numpy(self, queue):
        # copy cl to numpy
        self.narray = self.clarray.get()


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
    def __init__(self, queue, size, delta):
        # get values
        sizeX, sizeY = size
        deltaX, deltaY = delta

        # create even and odd Field
        self.evenFieldX = {
                'field': Buffer(queue, (sizeX / deltaX, sizeY / deltaY)),
                'flux': Buffer(queue, (sizeX / deltaX, sizeY / deltaY))}
        self.evenFieldY = {
                'field': Buffer(queue, (sizeX / deltaX, sizeY / deltaY)),
                'flux': Buffer(queue, (sizeX / deltaX, sizeY / deltaY))}
        self.oddFieldX = {
                'field': Buffer(queue, (sizeX / deltaX, sizeY / deltaY)),
                'flux': Buffer(queue, (sizeX / deltaX, sizeY / deltaY))}
        self.oddFieldY = {
                'field': Buffer(queue, (sizeX / deltaX, sizeY / deltaY)),
                'flux': Buffer(queue, (sizeX / deltaX, sizeY / deltaY))}

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
        return (self.evenFieldX['field'].narray[x, y],
                self.evenFieldY['field'].narray[x, y],
                self.oddFieldX['field'].narray[x, y] + \
                self.oddFieldY['field'].narray[x, y])
