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

    def __getitem__(self, key):
        """Returns the field vector at the given location"""
        # obtain parameter
        x, y = key

        # return field vector
        return self.evenFieldX['field'][x, y], self.evenFieldY['field'][x, y], self.oddGridX['field'][x, y] + self.oddGridY['field'][x, y]
