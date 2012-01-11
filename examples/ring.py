import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
from pyfdtd import *

# source function
@source
def f(t):
    x = t - 1000e-12
    return 1.0e3*math.exp(-x**2/(2.0*200.0e-12**2))*math.cos(2.0*math.pi*20e9*x)

# material function
def ring(x, y):
    if (x-0.2)**2 + (y-0.2)**2 < 0.13**2 or (x-0.2)**2 + (y-0.2)**2 > 0.15**2:
        return 1.0

    return 0.0

# progress function
history = []
def progress(t, deltaT, field):
    xShape, yShape = field.oddFieldX['flux'].shape
    interval = xShape*yShape*5e-9/(256e6/4.0)

    # save history
    if t/deltaT % (interval/deltaT) < 1.0:
        history.append(field.oddFieldX['field'] + field.oddFieldY['field'])

    # print progess
    if t/deltaT % 100 < 1.0:
        print '{}'.format(t*100.0/5e-9)

# create solver
solver = solver(field(0.4, 0.4, deltaX=0.001))

# add material
solver.material['electric'][ring] = material.epsilon(sigma=59.1e6)

# add source
solver.source[masks.ellipse(0.06, 0.2, 0.001)] = f

# iterate
solver.solve(5e-9, progressfunction=progress)

# show plot
fig = plt.figure(1)

ims = []
for f in history:
    im = plt.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 40.0))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
