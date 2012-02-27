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


import sys
import numpy
import pyopencl as cl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd


def main():
    # progress function
    history = []

    def progress(t, deltaT, field):
        xShape, yShape = field.oddFieldX['flux'].narray.shape
        interval = xShape * yShape * 5e-9 / (256e6 / 4.0)

        # save history
        if t / deltaT % (interval / deltaT) < 1.0:
            history.append((field.oddFieldX['field'].clarray + \
                    field.oddFieldY['field'].clarray).get())

        # print progess
        if t / deltaT % 100 < 1.0:
            print '{}'.format(t * 100.0 / 5e-9)

    # create context
    ctx = cl.create_some_context()

    # create queue
    queue = cl.CommandQueue(ctx)

    # create solver
    job = pyfdtd.Job().load(sys.argv[1])
    solver = job.get_solver(ctx, queue)

    # iterate
    solver.solve(queue, job.config['duration'], progressfunction=progress)

    # show plot
    fig = plt.figure(1)

    ims = []
    for f in history:
        im = plt.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 20.0))
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50)

    plt.show()

if __name__ == '__main__':
    main()
