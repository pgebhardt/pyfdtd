import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, epsilon, mu, sigma):
        self.oddGrid = {'epsilon': epsilon, 'mu': mu, 'sigma': sigma}

        # create even grid
        self.evenGrid = {}

        for key in self.oddGrid.iterkeys():
            # get shape
            xshape, yshape = self.oddGrid[key].shape

            # interpolate grid
            x = numpy.arange(0.5, xshape+0.5, 1.0)
            y = numpy.arange(0.5, yshape+0.5, 1.0)
            f = scipy.interpolate.interp2d(x, y, self.oddGrid[key].transpose(), kind='linear')

            # save data to oddGrid
            self.evenGrid[key] = numpy.zeros( (xshape+1, yshape+1) )
            for i in range(0, xshape+1, 1):
                for j in range(0, yshape+1, 1):
                    self.evenGrid[key][i, j] = f(i, j)
