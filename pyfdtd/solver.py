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


import math
import numpy
from scipy import constants
from material import Material
from field import Buffer
from pml import pml


class Solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, ctx, field, mode='TMz'):
        # save arguments
        self.field = field
        self.mode = mode
        self.ctx = ctx

        # create sources
        self.source = Material(self.ctx, field.size, field.delta)

        # create listeners
        self.listener = []

        # create materials
        self.material = {}
        self.material['electric'] = Material(self.ctx, field.size, field.delta)
        self.material['magnetic'] = Material(self.ctx, field.size, field.delta)

        # add free space layer
        self.material['electric'][:, :] = Material.epsilon()
        self.material['magnetic'][:, :] = Material.mu()

        # add pml layer
        #electric, magnetic, mask = pml(field.size, field.delta, mode=mode)
        #self.material['electric'][mask] = electric
        #self.material['magnetic'][mask] = magnetic

    def solve(self, queue, duration, starttime=0.0, deltaT=0.0,
            progressfunction=None, finishfunction=None):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # get parameter
        deltaX, deltaY = self.field.delta

        # calc deltaT
        if deltaT == 0.0:
            deltaT = 1.0 / (constants.c * math.sqrt(1.0 / \
                    deltaX ** 2 + 1.0 / deltaY ** 2))

        # create constants
        kx = deltaT / deltaX
        ky = deltaT / deltaY

        # material aliases
        material1 = 'electric'
        material2 = 'magnetic'

        # create source Buffer
        sourceX = Buffer(self.ctx,
                self.field.oddFieldX['field'].narray.shape)
        sourceY = Buffer(self.ctx,
                self.field.oddFieldX['field'].narray.shape)

        # apply mode
        if self.mode == 'TEz':
            kx, ky = -ky, -ky
            material1, material2 = material2, material1

        # iterate
        for t in numpy.arange(starttime, starttime + duration, deltaT):
            # do step
            self._step(queue, deltaT, t, kx, ky,
                    material1, material2, (sourceX, sourceY))

            # call all listeners
            for listener in self.listener:
                listener.update(self.field)

            # call progress function
            if progressfunction:
                progressfunction(t, deltaT, self.field)

        # call finish function
        if finishfunction:
            finishfunction()

    def _step(self, queue, deltaT, t, kx, ky, material1, material2, source):
        # calc oddField
        self.field.oddFieldY['flux'].narray[:-1, :-1] += kx * \
                (self.field.evenFieldY['field'].narray[1:, :-1] - \
                self.field.evenFieldY['field'].narray[:-1, :-1])
        self.field.oddFieldX['flux'].narray[:-1, :-1] -= ky * \
                (self.field.evenFieldX['field'].narray[:-1, 1:] - \
                self.field.evenFieldX['field'].narray[:-1, :-1])

        # apply sources
        #sourceX, sourceY = source
        #self.source.apply(queue,
        #        (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
        #        (sourceX, sourceY), deltaT, t)

        #sourceX.to_numpy()
        #sourceY.to_numpy()

        #self.field.oddFieldX['flux'].narray += sourceX.narray
        #self.field.oddFieldY['flux'].narray += sourceY.narray

        # apply material
        self.material[material1].apply(queue,
                (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
                (self.field.oddFieldX['field'], self.field.oddFieldY['field']),
                deltaT, t)

        # calc evenField
        self.field.evenFieldX['flux'].narray[:-1, 1:-1] -= ky * \
                (self.field.oddFieldX['field'].narray[:-1, 1:-1] + \
                self.field.oddFieldY['field'].narray[:-1, 1:-1] - \
                self.field.oddFieldX['field'].narray[:-1, :-2] - \
                self.field.oddFieldY['field'].narray[:-1, :-2])
        self.field.evenFieldY['flux'][1:-1, :-1] += kx * \
                (self.field.oddFieldX['field'].narray[1:-1, :-1] + \
                self.field.oddFieldY['field'].narray[1:-1, :-1] - \
                self.field.oddFieldX['field'].narray[:-2, :-1] - \
                self.field.oddFieldY['field'].narray[:-2, :-1])

        # apply material
        self.material[material2].apply(queue,
                (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
                (self.field.oddFieldX['field'], self.field.oddFieldY['field']),
                deltaT, t)
