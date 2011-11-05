import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # init grids
        xShape = xSize/deltaX
        yShape = ySize/deltaY

        self.oddGrid = {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape))}
        self.evenGridX = {'epsilon': numpy.ones((xShape, yShape+1)), 'mu': numpy.ones((xShape, yShape+1)), 'sigma': numpy.zeros((xShape, yShape+1))}
        self.evenGridY = {'epsilon': numpy.ones((xShape+1, yShape)), 'mu': numpy.ones((xShape+1, yShape)), 'sigma': numpy.zeros((xShape+1, yShape))}

        # save atributes
        self.xSize = xSize
        self.ySize = ySize
        self.deltaX = deltaX
        self.deltaY = deltaY

    def set_material(self, key, mat):
        xShape, yShape = mat.shape

        # save oddGrid
        self.oddGrid[key] = mat

        #interpolate evenGridX
        x = numpy.arange(0.5, xShape+0.5, 1.0)
        y = numpy.arange(0.5, yShape+0.5, 1.0)
        
