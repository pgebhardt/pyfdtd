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
solver = fdtd.solver(fdtd.grid(0.5, 0.5, 2.0, 2.0), fdtd.material(epsilon, mu, sigma), ports=[fdtd.port( (1.0, 1.0) )])

for port in solver.ports:
    print port.update(solver.grid)

solver.iterate(0.01, 100)
