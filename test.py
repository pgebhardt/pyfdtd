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

mat = fdtd.material(epsilon, mu, sigma)

for key in mat.oddGrid.iterkeys():
    print key, mat.oddGrid[key]
