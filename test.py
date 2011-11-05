import numpy
import scipy.interpolate
import matplotlib.pyplot as plt
import fdtd

epsilon = numpy.zeros( (4, 4) )
mu = numpy.zeros( (4, 4) )
sigma = numpy.zeros( (4, 4) )

xdim, ydim = epsilon.shape

for x1 in range(0, xdim, 1):
    for y1 in range(0, ydim, 1):
        epsilon[x1, y1] = x1*y1

# create listen ports
portlist = []
for i in range(1, 5, 1):
    portlist.append(fdtd.port( (i * 0.01, 0.01) ))

# add source port
def f(t):
    if t == 0.0:
        return 1.0
    else:
        return 0.0

portlist.append(fdtd.port( (0.025, 0.025), f))

# create solver
solver = fdtd.solver(fdtd.grid(0.05, 0.05, 0.001, 0.001), fdtd.material(0.05, 0.05, 0.001, 0.001), 
    ports=portlist)

# set materal
solver.material.set_material({'epsilon': epsilon, 'mu': mu, 'sigma': sigma})

# iterate
solver.iterate(0.5e-12, 500.0e-12)

#plot ports
plt.figure(1)

for port in solver.ports:
    plt.subplot(len(solver.ports), 1, solver.ports.index(port)+1)
    plt.plot(port.values)

plt.show()
