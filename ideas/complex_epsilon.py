import numpy
import pyfdtd

def inverse_epsilon(fl, dt):
    if not hasattr(inverse_epsilon, 'mem'):
        inverse_epsilon.mem = numpy.zeros(fl.shape)

    fi = (1.0/(pyfdtd.constants.e0*2.0 + 1.0*dt))*(fl - inverse_epsilon.mem)
    inverse_epsilon.mem += 1.0*fi*dt
    return fi

def form(x, y):
    if (x-4)**2 + (y-4)**2 < 2:
        return 1.0
    return 0.0

# flux, field
flux = numpy.ones((8, 8))*pyfdtd.constants.e0
field = numpy.ones((8, 8))

layer_mask = numpy.ones(flux.shape)

# layer mask
for i in range(0, 8, 1):
    for j in range(0, 8, 1):
        layer_mask[i, j] = form(i, j)

# calc field from flux
for i in range(0, 4, 1):
    field = inverse_epsilon(flux*layer_mask, 0.1e-9)
    print field
