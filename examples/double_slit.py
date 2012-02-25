import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd


# source function
@pyfdtd.source
def f(t):
    x = t - 1000e-12
    return 1.0e3 * math.exp(-x ** 2 / (2.0 * 200.0e-12 ** 2)) * \
            math.cos(2.0 * math.pi * 20e9 * x)


# mask functions
def slit(x, y):
    if y >= 0.58 and y <= 0.6:
        if (x >= 0.06 and x <= 0.07) or (x >= 0.13 and x <= 0.14):
            return 0.0

        else:
            return 1.0

    return 0.0


def lense(x, y):
    if (x - 0.1) ** 2 + (y - 0.2) ** 2 < 0.15 ** 2 and \
            (x - 0.1) ** 2 + (y - 0.4) ** 2 < 0.15 ** 2:
        return 1.0

    return 0.0

# progress function
history = []


def progress(t, deltaT, field):
    shapeX, shapeY = field.oddFieldX['flux'].shape
    interval = shapeX * shapeY * 5e-9 / (256e6 / 4.0)

    # save history
    if t / deltaT % (interval / deltaT) < 1.0:
        history.append(field.oddFieldX['field'] + field.oddFieldY['field'])

    # print progess
    if t / deltaT % 100 < 1.0:
        print '{}'.format(t * 100.0 / 5e-9)

# create solver
solver = pyfdtd.Solver(pyfdtd.Field((0.2, 0.8), (0.001, 0.001)))

# add material
solver.material['electric'][slit] = pyfdtd.Material.epsilon(sigma=59.1e6)
solver.material['electric'][lense] = pyfdtd.Material.epsilon(er=2.0)

# add source
solver.source[pyfdtd.masks.ellipse(0.1, 0.1, 0.001)] = f

# iterate
solver.solve(5e-9, progressfunction=progress)

# show plot
fig = plt.figure(1)

ims = []
for f in history:
    im = plt.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 10.0))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
