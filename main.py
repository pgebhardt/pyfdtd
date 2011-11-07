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
    return math.exp(-x**2/(2.0*50.0e-12**2))
    
portlist.append(fdtd.port( (0.009, 0.025), f))

# create solver
solver = fdtd.solver(fdtd.field(0.05, 0.05, 0.0005, 0.0005), ports=portlist)

# iterate
solver.iterate(1.0e-12, 2000e-12)

# plot ports
plt.figure(1)

for i in range(0, 3, 1):
    plt.subplot(4, 1, i+1)
    plt.title = portlist[i].position
    plt.plot(portlist[i].values)

plt.subplot(4, 1, 4)

mask = numpy.zeros((100, 100))

a = solver.field.oddFieldX['field'] + solver.field.oddFieldY['field']
plt.imshow(a)

plt.show()
