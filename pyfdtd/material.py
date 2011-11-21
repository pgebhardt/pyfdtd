from types import *
import copy
import numpy
from constants import constants
import field as fi

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # save atributes
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize

        # create layer list
        self.layer = []

    def __setitem__(self, key, value):
        """
        Creates a new material layer using key as mask
        and value as material function
        """
        # create mask
        mask = numpy.zeros((self.xSize/self.deltaX, self.ySize/self.deltaY))

        # check if key is not a function
        if not isinstance(key, FunctionType):
            key = material._helper.scale_slice(key, self.deltaX, self.deltaY)

            # evaluate slice
            ones = numpy.ones((self.xSize/self.deltaX, self.ySize/self.deltaY))
            mask[key] = ones[key]

        else:
            # evaluate mask function
            mask = numpy.zeros((self.xSize/self.deltaX, self.ySize/self.deltaY))
            for x in range(0, int(self.xSize/self.deltaX), 1):
                for y in range(0, int(self.ySize/self.deltaY), 1):
                    mask[x, y] = key(x*self.deltaX, y*self.deltaY)
    
        # check if value is a function
        if not isinstance(value, FunctionType):
            v = copy.deepcopy(value)
            value = lambda flux, dt: v
             
        # add new layer
        self.layer.append((copy.deepcopy(value), mask))

    def apply(self, flux, deltaT):
        """
        Calculate field from flux density
        """
        # create field
        field = numpy.zeros(flux.shape)

        # apply all layer
        for layer in self.layer:
            func, mask = layer

            # calc field
            field = func(flux*mask, deltaT) + (1.0-mask)*field

        return field

    class _helper:
        """
        Helper functions for internal use
        """
        @staticmethod
        def scale_slice(key, deltaX, deltaY):
            x, y = key

            # scale slices
            if x.start:
                x = slice(x.start/deltaX, x.stop)
            if x.stop:
                x = slice(x.start, x.stop/deltaX)
            if y.start:
                y = slice(y.start/deltaY, y.stop)
            if y.stop:
                y = slice(y.start, y.stop/deltaY)

            return x, y

    class standart:
        """
        Defines a couple a standart material functions
        """
        @staticmethod
        def epsilon(er=1.0, sigma=0.0):
            # create epsilon function
            def res(flux, dt):              
                # check if mem already exists
                if not hasattr(res, 'mem'):
                    res.mem = numpy.zeros(flux.shape)

                field = (1.0/(constants.e0*er + sigma*dt))*(flux - res.mem)
                res.mem += sigma*field*dt
                return field

            # return function
            return res

        @staticmethod
        def mu(mur=1.0):
            # create mu function
            def res(flux, dt):
                return flux/(constants.mu0*mur)

            # return function
            return res

if __name__ == '__main__':
    flux = numpy.ones((20, 20))*constants.e0
    mat = material(1.0, 1.0, 0.05, 0.05)
    mat[0.2:0.6,0.2:0.6] = material.standart.epsilon()
    field = mat.apply(flux, 0.1)
    print field
