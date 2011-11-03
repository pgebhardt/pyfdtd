import numpy
import scipy.interpolate

class grid:
    """Defines the calculation domain"""
    def __init__(self, deltaX, deltaY, xSize, ySize):
        self.hField = numpy.zeros( (xSize/deltaX, ySize/deltaY) )
        self.eField = numpy.zeros( (xSize/deltaX, ySize/deltaY) )
        
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize
