import numpy
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import fdtd

epsilon = numpy.zeros( (4, 4) )
mu = numpy.zeros( (4, 4) )
sigma = numpy.zeros( (4, 4) )

xdim, ydim = epsilon.shape

for x1 in range(0, xdim, 1):
    for y1 in range(0, ydim, 1):
        epsilon[x1, y1] = x1*y1

# createports
portlist = []
for i in range(1, 5, 1):
    portlist.append(fdtd.port( (i * 0.01, 0.01) ))

# create solver
solver = fdtd.solver(fdtd.grid(0.001, 0.001, 0.05, 0.05), fdtd.material(epsilon, mu, sigma), ports=portlist)
solver.grid.oddGrid[25, 25] = 1.0

solver.iterate(1.0e-12, 100)

plt.figure(1)

for port in solver.ports:
    plt.subplot(len(solver.ports), 1, solver.ports.index(port)+1)
    plt.plot(port.values)

plt.show()
