import math
import numpy
import numpy.ma
import scipy.interpolate
import matplotlib.pyplot as plt
import fdtd

# create listen ports
portlist = []

# add source port
def f(t):
    x = t - 300e-12
    if x < 0.0:
        return math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    elif x < 600e-12:
        return math.cos(2.0*math.pi*40e9*x)
    else:
        return math.exp(-(x-600e-12)**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    
portlist.append(fdtd.port( (0.01, 0.01), f))

# create solver
solver = fdtd.solver(fdtd.field(0.05, 0.20, 0.0005, 0.0005), ports=portlist)

# add material
layer = solver.material.empty_layer()

for i in range(0, 20, 1):
    for j in range(0, 20, 1):
        layer['epsilon'][40+i, 360+j] = 8.0

solver.material.add_layer(layer)

# iterate
solver.iterate(1.0e-12, 300e-12)

# plot ports
plt.figure(1)

for port in portlist:
    plt.subplot(len(portlist)+1, 1, portlist.index(port)+1)
    plt.plot(port.values)

plt.subplot(len(portlist)+1, 1, len(portlist)+1)

plt.imshow(solver.field.oddFieldX['field'] + solver.field.oddFieldY['field'])

plt.show()
