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

# create solver
solver = solver(field(0.2, 0.4, deltaX=0.001))

# add material
solver.material['electric'][:,:] = material.epsilon(sigma=59.1e6)
solver.material['electric'][0.07:0.13,0.05:-0.05] = material.epsilon()

# add source
solver.source[masks.ellipse(0.1, 0.1, 0.001)] = f

# iterate
history = solver.solve(5e-9, saveHistory=True)

# show plot
fig = plt.figure(1)

ims = []
for f in history:
    im = plt.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 20.0))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
