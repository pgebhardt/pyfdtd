import numpy
import scipy.interpolate
import fdtd

epsilon = numpy.zeros( (4, 4) )
mu = numpy.zeros( (4, 4) )
sigma = numpy.zeros( (4, 4) )

xdim, ydim = epsilon.shape

for x1 in range(0, xdim, 1):
    for y1 in range(0, ydim, 1):
        epsilon[x1, y1] = x1*y1

# create solver
solver = fdtd.solver(fdtd.grid(0.001, 0.001, 0.05, 0.05), fdtd.material(epsilon, mu, sigma), ports=[fdtd.port( (0.025, 0.025) )])
solver.grid.oddGrid[5, 5] = 1.0

for i in range(0, 1000, 1):
    solver.iterate(1.0e-12, 1)

    for port in solver.ports:
        print port.value
