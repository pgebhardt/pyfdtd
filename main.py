import math
import numpy
import numpy.ma
import scipy.interpolate
import matplotlib.pyplot as plt
import fdtd

# create listen ports
portlist = []

for i in range(0, 2, 1):
    portlist.append(fdtd.port((0.02 + i*0.01, 0.02)))

# add source port
def f(t):
    x = t - 300e-12
    return math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    
portlist.append(fdtd.port( (0.025, 0.025), f))

# create solver
solver = fdtd.solver(fdtd.field(0.05, 0.05, 0.0005, 0.0005), ports=portlist)

# iterate
solver.iterate(1.0e-12, 500e-12)

# plot ports
plt.figure(1)

for port in portlist:
    plt.subplot(len(portlist)+1, 1, portlist.index(port)+1)
    plt.plot(port.values)

plt.subplot(4, 1, 4)

a = solver.field.oddFieldX['field'] + solver.field.oddFieldY['field']
plt.imshow(a)

plt.show()
