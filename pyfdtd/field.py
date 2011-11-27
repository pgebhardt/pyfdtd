import numpy

class field:
    """
    Defines the calculation domain by creating even and odd yee grids
    for field and flux.

        **Arguments:**

    xSize (required)
        Size in x direction

    ySize (required)
        Size in y direction

    deltaX (required)
        Interval of discretization in x direction

    deltaY
        Interval if discretization in y direction. If not set, deltaX is used instead.
    """
    def __init__(self, xSize, ySize, deltaX, deltaY=None):
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

        # scale x, y
        x, y = int(x/self.deltaX), int(y/self.deltaY)

        # return field vector
        return self.evenFieldX['field'][x, y], self.evenFieldY['field'][x, y], self.oddGridX['field'][x, y] + self.oddGridY['field'][x, y]
