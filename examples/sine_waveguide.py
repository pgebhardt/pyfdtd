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
    return 40.0 * math.exp(-x ** 2 / (2.0 * 50.0e-12 ** 2)) * \
            math.cos(2.0 * math.pi * 20e9 * x)


# material function
def surface1(x, y):
    if x - 0.02 * math.sin(2.0 * math.pi * 8.0 * y) - 0.1 > 0.0:
        return 1.0

    return 0.0


def surface2(x, y):
    if x - 0.02 * math.sin(2.0 * math.pi * 8.0 * y) - 0.08 < 0.0:
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
solver = pyfdtd.Solver(pyfdtd.Field((0.2, 0.4), (0.001, 0.001)))

# add material
solver.material['electric'][surface1] = pyfdtd.Material.epsilon(sigma=59.1e6)
solver.material['electric'][surface2] = pyfdtd.Material.epsilon(sigma=59.1e6)

# add source
solver.source[pyfdtd.masks.ellipse(0.1, 0.05, 5, 0.001)] = f

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
