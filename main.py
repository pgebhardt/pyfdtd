import math
import numpy
import scipy.interpolate
import matplotlib.pyplot as plt
import fdtd

# create listen ports
portlist = []

# add source port
def f(t):
    x = t - 300e-12
    return math.exp(-x**2/(2.0*50.0e-12**2))
    
portlist.append(fdtd.port( (0.025, 0.025), f))

# create solver
solver = fdtd.solver(fdtd.field(0.05, 0.05, 0.001, 0.001), ports=portlist)

# create material
epsilon = numpy.ones((50, 50))

for x in range(40, 50, 1):
    for y in range(20, 30, 1):
        epsilon[x, y] = 10.0

# solver.material['epsilon'] = epsilon

# iterate
solver.iterate(1.0e-12, 500e-12)

# plot ports
plt.figure(1)

plt.subplot(2, 1, 1)
plt.plot(portlist[0].values)

plt.subplot(2, 1, 2)
plt.imshow(solver.field.oddFieldX['flux'] + solver.field.oddFieldY['flux'])

plt.show()
