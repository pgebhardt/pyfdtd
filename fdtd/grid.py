import numpy
import scipy.interpolate

class grid:
    """Defines the calculation domain"""
    def __init__(self, deltaX, deltaY, xSize, ySize):
        # create even and odd Grid
        self.evenGridX = numpy.zeros( (xSize/deltaX, ySize/deltaY) )
        self.evenGridY = numpy.zeros( (xSize/deltaX, ySize/deltaY) )
        self.oddGrid = numpy.zeros( (xSize/deltaX - 1, ySize/deltaY - 1) )
        
        # save all given information
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize
