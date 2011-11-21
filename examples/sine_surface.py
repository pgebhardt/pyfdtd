import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd

# source function
def f(t):
    x = t - 1000e-12
    return 10.0e3*math.exp(-x**2/(2.0*200.0e-12**2))*math.cos(2.0*math.pi*20e9*x)

# material function
def surface(x, y):
    if x - 0.02*math.sin(2.0*math.pi*8.0*y) - 0.3 > 0.0:
        return 1.0

    return 0.0

# create solver
solver = pyfdtd.solver(pyfdtd.field(0.4, 0.4, deltaX=0.001))

# add material
solver.material['electric'][surface] = pyfdtd.material.epsilon(sigma=59.1e6)

# add source
solver.ports.append(pyfdtd.port(0.1, 0.2, source=f))

# iterate
history = solver.solve(5e-9, saveHistory=True)

# show plot
fig = plt.figure(1)

ims = []
for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-0.015e-8, 0.015e-8))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
