import numpy
import scipy.interpolate

class field:
    """Defines the calculation domain"""
    def __init__(self, xSize, ySize, deltaX, deltaY=None):
        """Creates am new field with given size and discretization"""
        # fill missing parameters
        if not deltaY:
            deltaY = deltaX

        # create even and odd Field
        self.evenFieldX = { 'field': numpy.zeros((xSize/deltaX, ySize/deltaY)), 'flux': numpy.zeros((xSize/deltaX, ySize/deltaY)) }
        self.evenFieldY = { 'field': numpy.zeros((xSize/deltaX, ySize/deltaY)), 'flux': numpy.zeros((xSize/deltaX, ySize/deltaY)) }
        self.oddFieldX = { 'field': numpy.zeros((xSize/deltaX, ySize/deltaY)), 'flux': numpy.zeros((xSize/deltaX, ySize/deltaY)) }
        self.oddFieldY = { 'field': numpy.zeros((xSize/deltaX, ySize/deltaY)), 'flux': numpy.zeros((xSize/deltaX, ySize/deltaY)) }
        
        # save all given information
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.xSize = xSize
        self.ySize = ySize

    def get_field(self, x, y, key='field'):
        """Returns the field vector at the given location"""
        return self.evenFieldX[key][x, y], self.evenFieldY[key][x, y], self.oddGridX[key][x, y] + self.oddGridY[key][x, y]
