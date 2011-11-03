import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, epsilon, mu, sigma):
        self.evenGrid = {'epsilon': epsilon, 'mu': mu, 'sigma': sigma}

        # create odd grid
        self.oddGrid = {}

        for key in self.evenGrid.iterkeys():
            # get shape
            xshape, yshape = self.evenGrid[key].shape

            # interpolate grid
            x = numpy.arange(0.0, xshape, 1.0)
            y = numpy.arange(0.0, yshape, 1.0)
            f = scipy.interpolate.interp2d(x, y, self.evenGrid[key].transpose(), kind='linear')

            # save data to oddGrid
            self.oddGrid[key] = numpy.zeros( (xshape-1, yshape-1) )
            for i in range(0, xshape-1, 1):
                for j in range(0, yshape-1, 1):
                    self.oddGrid[key][i, j] = f(i+0.5, j+0.5)
