import numpy
import pyfdtd
import copy

def inverse_epsilon(fl, dt, eps, sig):
    if not hasattr(inverse_epsilon, 'mem'):
        inverse_epsilon.mem = numpy.zeros(fl.shape)

    fi = (1.0/(pyfdtd.constants.e0*eps + sig*dt))*(fl - inverse_epsilon.mem)
    inverse_epsilon.mem += sig*fi*dt
    return fi

def form(x, y):
    if (x-4)**2 + (y-4)**2 < 2:
        return 1.0
    return 0.0

# flux, field
flux = numpy.ones((8, 8))*pyfdtd.constants.e0
field = numpy.ones((8, 8))

layer_mask = numpy.ones(flux.shape)

# layer dict
layer = {}

# add epsilon layer
layer['epsilon'] = (copy.deepcopy(lambda fl, dt: inverse_epsilon(fl, dt, 1.0, 0.0)), copy.deepcopy(lambda x, y: 1.0))
layer['cube'] = (copy.deepcopy(lambda fl, dt: inverse_epsilon(fl, dt, 2.0, 1.0)), copy.deepcopy(form))

# clear field
field = 0.0*field

# apply layer
for value in layer.itervalues():
    func, mask = value

    # layer mask
    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            layer_mask[i, j] = mask(i, j)

    # calc field from flux
    field += func(flux*layer_mask, 0.1e-9)

print field
