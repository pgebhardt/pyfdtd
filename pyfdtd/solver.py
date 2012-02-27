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
import pyopencl as cl
from scipy import constants
from material import Material
from pml import pml


class Solver:
    """Solves FDTD equations on given field, with given materials and ports"""
    def __init__(self, ctx, queue, field, mode='TMz'):
        # save arguments
        self.field = field
        self.mode = mode
        self.ctx = ctx
        self.queue = queue

        # create sources
        self.source = Material(self.queue, field.size, field.delta)

        # create listeners
        self.listener = []

        # create materials
        self.material = {}
        self.material['electric'] = Material(self.queue,
                field.size, field.delta)
        self.material['magnetic'] = Material(self.queue,
                field.size, field.delta)

        # add free space layer
        self.material['electric'][:, :] = Material.epsilon()
        self.material['magnetic'][:, :] = Material.mu()

        # add pml layer
        electric, magnetic, mask = pml(self.queue,
                field.size, field.delta, mode=mode)
        self.material['electric'][mask] = electric
        self.material['magnetic'][mask] = magnetic

        # create programs
        self.create_programs()

    def create_programs(self):
        self.program = cl.Program(self.ctx,
                """__kernel void oddFieldX(""" + \
                """__global float* oddFieldX,""" + \
                """__global const float* evenFieldX)""" + \
                """{""" + \
                """    int x = get_global_id(0);""" + \
                """    int y_size = get_global_size(1);""" + \
                """    int y = get_global_id(1);""" + \
                """    oddFieldX[x*y_size + y] += """ + \
                """        evenFieldX[x*y_size + y+1] + """ + \
                """        evenFieldX[x*y_size + y];""" + \
                """}""")

        # build
        try:
            self.program.build()
        except:
            print("Error:")
            print(self.program.get_build_info(self.ctx.devices[0],
                cl.program_build_info.LOG))
            raise

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

        # apply mode
        if self.mode == 'TEz':
            kx, ky = -ky, -ky
            material1, material2 = material2, material1

        # iterate
        for t in numpy.arange(starttime, starttime + duration, deltaT):
            # do step
            self._step(queue, deltaT, t, kx, ky, material1, material2)

            # call all listeners
            for listener in self.listener:
                listener.update(self.field)

            # call progress function
            if progressfunction:
                progressfunction(t, deltaT, self.field)

        # call finish function
        if finishfunction:
            finishfunction()

    def _step(self, queue, deltaT, t, kx, ky, material1, material2):
        # sync Buffer
        self.field.oddFieldX['flux'].to_numpy(queue)
        self.field.oddFieldY['flux'].to_numpy(queue)
        self.field.evenFieldX['field'].to_numpy(queue)
        self.field.evenFieldY['field'].to_numpy(queue)

        # calc oddField
        self.field.oddFieldY['flux'].narray[:-1, :-1] += kx * \
                (self.field.evenFieldY['field'].narray[1:, :-1] - \
                self.field.evenFieldY['field'].narray[:-1, :-1])

        self.field.oddFieldX['flux'].narray[:-1, :-1] -= ky * \
                (self.field.evenFieldX['field'].narray[:-1, 1:] - \
                self.field.evenFieldX['field'].narray[:-1, :-1])

        shapeX, shapeY = self.field.oddFieldX['flux'].narray.shape
        self.program.oddFieldX(self.queue, (shapeX - 1, shapeY - 1),
                None, self.field.oddFieldX['flux'].clarray.data,
                self.field.evenFieldX['field'].clarray.data)

        print self.field.oddFieldX['flux'].clarray.get()[100, 100]

        # sync Buffer
        self.field.oddFieldX['flux'].to_cl(queue)
        self.field.oddFieldY['flux'].to_cl(queue)

        # apply sources
        sourceX, sourceY = self.source.apply(queue,
                (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
                deltaT, t)

        self.field.oddFieldX['flux'].clarray += sourceX
        self.field.oddFieldY['flux'].clarray += sourceY

        # apply material
        (self.field.oddFieldX['field'].clarray,
            self.field.oddFieldY['field'].clarray) = \
                self.material[material1].apply(queue,
                    (self.field.oddFieldX['flux'],
                        self.field.oddFieldY['flux']),
                        deltaT, t)

        # sync Buffer
        self.field.evenFieldX['flux'].to_numpy(queue)
        self.field.evenFieldY['flux'].to_numpy(queue)
        self.field.oddFieldX['field'].to_numpy(queue)
        self.field.oddFieldY['field'].to_numpy(queue)

        # calc evenField
        self.field.evenFieldX['flux'].narray[:-1, 1:-1] -= ky * \
                (self.field.oddFieldX['field'].narray[:-1, 1:-1] + \
                self.field.oddFieldY['field'].narray[:-1, 1:-1] - \
                self.field.oddFieldX['field'].narray[:-1, :-2] - \
                self.field.oddFieldY['field'].narray[:-1, :-2])
        self.field.evenFieldY['flux'].narray[1:-1, :-1] += kx * \
                (self.field.oddFieldX['field'].narray[1:-1, :-1] + \
                self.field.oddFieldY['field'].narray[1:-1, :-1] - \
                self.field.oddFieldX['field'].narray[:-2, :-1] - \
                self.field.oddFieldY['field'].narray[:-2, :-1])

        # sync Buffer
        self.field.evenFieldX['flux'].to_cl(queue)
        self.field.evenFieldY['flux'].to_cl(queue)

        # apply material
        (self.field.evenFieldX['field'].clarray,
            self.field.evenFieldY['field'].clarray) = \
                self.material[material2].apply(queue,
                    (self.field.evenFieldX['flux'],
                        self.field.evenFieldY['flux']),
                        deltaT, t)
