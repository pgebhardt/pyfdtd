import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd

# source function
def f(t):
    x = t - 1000e-12
    return 1.0e3*math.exp(-x**2/(2.0*200.0e-12**2))*math.cos(2.0*math.pi*20e9*x)

# mask functions
def slit(x, y):
    if y >= 0.58 and y <= 0.6:
        if (x >= 0.06 and x <= 0.07) or (x >= 0.13 and x <= 0.14):
            return 0.0

        else:
            return 1.0

    return 0.0

def lense(x, y):
    if (x-0.1)**2 + (y-0.2)**2 < 0.15**2 and (x-0.1)**2 + (y-0.4)**2 < 0.15**2:
        return 1.0

    return 0.0

# create solver
solver = pyfdtd.solver(pyfdtd.field(0.2, 0.8, deltaX=0.001))

# add material
solver.material['electric'][slit] = pyfdtd.material.epsilon(sigma=59.1e6)
solver.material['electric'][lense] = pyfdtd.material.epsilon(er=2.0)

# add source
solver.ports.append(pyfdtd.port(0.1, 0.1, source=f))

# iterate
history = solver.solve(5e-9, saveHistory=True)

# show plot
fig = plt.figure(1)

ims = []
for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-10.0, 10.0))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
