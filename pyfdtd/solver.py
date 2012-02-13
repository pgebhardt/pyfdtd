# pyfdtd is a simple 2d fdtd using numpy
# Copyright (C) 2012  Patrik Gebhardt
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
from constants import constants
from material import material
from pml import pml


class solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, field, mode='TMz'):
        # save arguments
        self.field = field
        self.mode = mode

        # create sources
        self.source = material(field.size, field.delta)

        # create listeners
        self.listener = []

        # create materials
        self.material = {}
        self.material['electric'] = material(field.size, field.delta)
        self.material['magnetic'] = material(field.size, field.delta)

        # add free space layer
        self.material['electric'][:, :] = material.epsilon()
        self.material['magnetic'][:, :] = material.mu()

        # add pml layer
        electric, magnetic, mask = pml(field.size, field.delta, mode=mode)
        self.material['electric'][mask] = electric
        self.material['magnetic'][mask] = magnetic

    def solve(self, duration, starttime=0.0, deltaT=0.0,
            progressfunction=None, finishfunction=None):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # get parameter
        deltaX, deltaY = self.field.delta

        # calc deltaT
        if deltaT == 0.0:
            deltaT = 1.0 / (constants.c0 * math.sqrt(1.0 / \
                    deltaX ** 2 + 1.0 / deltaY ** 2))

        # create constants
        kx = deltaT / deltaX
        ky = deltaT / deltaY

        # apply mode
        if self.mode == 'TEz':
            kx, ky = -ky, -ky

        # iterate
        for t in numpy.arange(starttime, starttime + duration, deltaT):
            # do step
            self._step(deltaT, t, kx, ky)

            # call all listeners
            for listener in self.listener:
                listener.update(self.field)

            # call progress function
            if progressfunction:
                progressfunction(t, deltaT, self.field)

        # call finish function
        if finishfunction:
            finishfunction()

    def _step(self, deltaT, t, kx, ky):
        # calc oddField
        self.field.oddFieldY['flux'][:-1, :-1] += kx * \
                (self.field.evenFieldY['field'][1:, :-1] - \
                self.field.evenFieldY['field'][:-1, :-1])
        self.field.oddFieldX['flux'][:-1, :-1] -= ky * \
                (self.field.evenFieldX['field'][:-1, 1:] - \
                self.field.evenFieldX['field'][:-1, :-1])

        # apply sources
        sourceX, sourceY = self.source.apply((self.field.oddFieldX['flux'],
            self.field.oddFieldY['flux']), deltaT, t)
        self.field.oddFieldX['flux'] += sourceX
        self.field.oddFieldY['flux'] += sourceY

        # apply material
        if self.mode == 'TMz':
            self.field.oddFieldX['field'], self.field.oddFieldY['field'] = \
                    self.material['electric'].apply(
                            (self.field.oddFieldX['flux'],
                                self.field.oddFieldY['flux']), deltaT, t)
        elif self.mode == 'TEz':
            self.field.oddFieldX['field'], self.field.oddFieldY['field'] = \
                    self.material['magnetic'].apply(
                            (self.field.oddFieldX['flux'],
                                self.field.oddFieldY['flux']), deltaT, t)

        # calc evenField
        self.field.evenFieldX['flux'][:-1, 1:-1] -= ky * \
                (self.field.oddFieldX['field'][:-1, 1:-1] + \
                self.field.oddFieldY['field'][:-1, 1:-1] - \
                self.field.oddFieldX['field'][:-1, :-2] - \
                self.field.oddFieldY['field'][:-1, :-2])
        self.field.evenFieldY['flux'][1:-1, :-1] += kx * \
                (self.field.oddFieldX['field'][1:-1, :-1] + \
                self.field.oddFieldY['field'][1:-1, :-1] - \
                self.field.oddFieldX['field'][:-2, :-1] - \
                self.field.oddFieldY['field'][:-2, :-1])

        # apply material
        if self.mode == 'TMz':
            self.field.evenFieldX['field'], self.field.evenFieldY['field'] = \
                    self.material['magnetic'].apply(
                            (self.field.evenFieldX['flux'],
                                self.field.evenFieldY['flux']), deltaT, t)
        elif self.mode == 'TEz':
            self.field.evenFieldX['field'], self.field.evenFieldY['field'] = \
                    self.material['electric'].apply(
                            (self.field.evenFieldX['flux'],
                                self.field.evenFieldY['flux']), deltaT, t)
