import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # init grids
        xShape = xSize/deltaX
        yShape = ySize/deltaY

        self.oddGrid = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape))}
        self.evenGridX = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape))}
        self.evenGridY = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape))}

        # save atributes
        self.xSize = xSize
        self.ySize = ySize
        self.deltaX = deltaX
        self.deltaY = deltaY

    def set_material(self, key, material):
        pass
