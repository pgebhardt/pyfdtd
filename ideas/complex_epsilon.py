from types import *
import numpy
import pyfdtd
import copy

class material:
    def __init__(self, xSize, ySize, deltaX, deltaY, mode='TMz'):
        self.layer = {}

    def __setitem__(self, key, value):
        # check weather value is a function
        if not isinstance(value, FunctionType):
            a = copy.deepcopy(value)
            value = lambda fl, dt: a*fl

        self.layer[key] = value

mat = material(1.0, 1.0, 0.1, 0.1)
mat['bla'] = 1.0/pyfdtd.constants.e0
print mat.layer['bla'](pyfdtd.constants.e0, 0.0)

def standart(fl, dt, a, b):
    if not hasattr(standart, 'mem'):
        standart.mem = numpy.zeros(fl.shape)

    fi = (1.0/(pyfdtd.constants.e0*a + b*dt))*(fl - standart.mem)
    standart.mem += b*fi*dt
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
layer['epsilon'] = (copy.deepcopy(lambda fl, dt: standart(fl, dt, 1.0, 0.0)), copy.deepcopy(lambda fl, dt: standart(fl, dt, 1.0, 0.0)), copy.deepcopy(lambda x, y: 1.0))
layer['cube'] = (copy.deepcopy(lambda fl, dt: standart(fl, dt, 2.0, 1.0)), copy.deepcopy(lambda fl, dt: standart(fl, dt, 1.0, 0.0)), copy.deepcopy(form))

# clear field
field = 0.0*field

# apply layer
for value in layer.itervalues():
    funcE, funcH, mask = value

    # layer mask
    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            layer_mask[i, j] = mask(i, j)

    # calc field from flux
    field = funcE(flux*layer_mask, 0.1e-9) + (1.0-layer_mask)*field

print field
