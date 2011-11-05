import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # init grids
        xShape = xSize/deltaX
        yShape = ySize/deltaY

        self.oddGrid = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape))}
        self.evenGridX = {'epsilon': numpy.ones((xShape+1, yShape+1)), 'mu': numpy.ones((xShape+1, yShape+1)), 'sigma': numpy.zeros((xShape+1, yShape+1))}
        self.evenGridY = {'epsilon': numpy.ones((xShape+1, yShape+1)), 'mu': numpy.ones((xShape+1, yShape+1)), 'sigma': numpy.zeros((xShape+1, yShape+1))}

        # save atributes
        self.xSize = xSize
        self.ySize = ySize
        self.deltaX = deltaX
        self.deltaY = deltaY

    def set_material(self, key, material):
        pass
