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


import os
import inspect
import math
import numpy
import pyopencl as cl
import pyopencl.array as clarray
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
        self.source = Material(self.ctx, self.queue, field.size, field.delta)
        self.sourceX = clarray.to_device(self.queue,
            numpy.zeros(self.field.oddFieldX['flux'].shape))
        self.sourceY = clarray.to_device(self.queue,
            numpy.zeros(self.field.oddFieldY['flux'].shape))

        # create listener
        self.listener = []

        # create materials
        self.material = {}
        self.material['electric'] = Material(self.ctx, self.queue,
                field.size, field.delta)
        self.material['magnetic'] = Material(self.ctx, self.queue,
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
        # open file
        pathName = os.path.dirname(inspect.getfile(inspect.currentframe()))
        f = open(pathName + '/solver_kernel.cl', 'r')

        # read string
        programmString = f.read()

        # create program
        self.program = cl.Program(self.ctx, programmString)

        # build
        try:
            self.program.build()
        except:
            print("Error:")
            print(self.program.get_build_info(self.ctx.devices[0],
                cl.program_build_info.LOG))
            raise
        finally:
            # close file
            f.close()

    def solve(self, duration, starttime=0.0, deltaT=0.0,
            progressfunction=None, finishfunction=None):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # get parameter
        deltaX, deltaY = self.field.delta
        shapeX, shapeY = self.field.oddFieldX['flux'].shape

        # calc deltaT
        if deltaT == 0.0:
            deltaT = 1.0 / (constants.c * math.sqrt(1.0 / \
                    deltaX ** 2 + 1.0 / deltaY ** 2))

        # create constants
        kx = deltaT / deltaX
        ky = deltaT / deltaY

        # create listener memory
        for listener in self.listener:
            listener.clvalues = clarray.to_device(self.queue,
                numpy.zeros((duration / deltaT + 1, 3)))

        # material aliases
        material1 = 'electric'
        material2 = 'magnetic'

        # apply mode
        if self.mode == 'TEz':
            kx, ky = -ky, -ky
            material1, material2 = material2, material1

        # iterate
        timerange = map(None, numpy.arange(starttime, starttime + duration,
            deltaT))

        for t in timerange:
            # do step
            self._step(deltaT, t, kx, ky, material1, material2)

            # call all listeners
            step = numpy.int32(timerange.index(t))

            for listener in self.listener:
                # finish queue
                self.queue.finish()

                # get listener position
                posX, posY = listener.pos

                # save field at listener position
                self.program.listener(self.queue, (1, ), None,
                    listener.clvalues.data,
                    self.field.evenFieldX['field'].data,
                    self.field.evenFieldX['field'].data,
                    self.field.oddFieldX['field'].data,
                    self.field.oddFieldY['field'].data,
                    numpy.int32(int(posX * shapeY / deltaX) + \
                        int(posY / deltaY)),
                    step)

            # call progress function
            if progressfunction:
                progressfunction(t, deltaT, self.field)

        # copy all listener to host
        for listener in self.listener:
            listener.copy_to_host()

        # call finish function
        if finishfunction:
            finishfunction()

    def _step(self, deltaT, t, kx, ky, material1, material2):
        shapeX, shapeY = self.field.oddFieldX['flux'].shape
        eventX = self.program.oddFieldX(self.queue, (shapeX - 1, shapeY - 1),
                None, self.field.oddFieldX['flux'].data,
                self.field.evenFieldX['field'].data, numpy.float64(ky))

        eventY = self.program.oddFieldY(self.queue, (shapeX - 1, shapeY - 1),
                None, self.field.oddFieldY['flux'].data,
                self.field.evenFieldY['field'].data, numpy.float64(kx))

        eventX.wait()
        eventY.wait()

        # apply sources
        self.source.apply(self.queue,
            (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
            (self.sourceX, self.sourceY), deltaT, t)

        self.field.oddFieldX['flux'] += self.sourceX
        self.field.oddFieldY['flux'] += self.sourceY

        # apply material
        self.material[material1].apply(self.queue,
            (self.field.oddFieldX['flux'], self.field.oddFieldY['flux']),
            (self.field.oddFieldX['field'], self.field.oddFieldY['field']),
            deltaT, t)

        eventX = self.program.evenFieldX(self.queue, (shapeX - 1, shapeY - 2),
                None, self.field.evenFieldX['flux'].data,
                self.field.oddFieldX['field'].data,
                self.field.oddFieldY['field'].data, numpy.float64(ky))

        eventY = self.program.evenFieldY(self.queue, (shapeX - 2, shapeY - 1),
                None, self.field.evenFieldY['flux'].data,
                self.field.oddFieldX['field'].data,
                self.field.oddFieldY['field'].data, numpy.float64(kx))

        eventX.wait()
        eventY.wait()

        # apply material
        self.material[material2].apply(self.queue,
            (self.field.evenFieldX['flux'], self.field.evenFieldY['flux']),
            (self.field.evenFieldX['field'], self.field.evenFieldY['field']),
            deltaT, t)
