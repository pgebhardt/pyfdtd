import numpy
import scipy.interpolate

class grid:
    """Defines the calculation domain"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # create even and odd Grid
        self.evenGridX = { 'field': numpy.zeros( (xSize/deltaX+1, ySize/deltaY+1) ), 'flux': numpy.zeros( (xSize/deltaX+1, ySize/deltaY+1) ) }
        self.evenGridY = { 'field': numpy.zeros( (xSize/deltaX+1, ySize/deltaY+1) ), 'flux': numpy.zeros( (xSize/deltaX+1, ySize/deltaY+1) ) }
        self.oddGrid = { 'field': numpy.zeros( (xSize/deltaX, ySize/deltaY) ), 'flux': numpy.zeros( (xSize/deltaX, ySize/deltaY) ) }
        
        # save all given information
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize
