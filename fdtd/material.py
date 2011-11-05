import numpy
import scipy.interpolate

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # init grids
        self.oddGrid = {}
        self.evenGridX = {}
        self.evenGridY = {}

        # save atributes
        self.xSize = xSize
        self.ySize = ySize
        self.deltaX = deltaX
        self.deltaY = deltaY

    def set_material(self, material):
        # fill odd Grid
        for key in material.iterkeys():
            xShape, yShape = material[key].shape
            
            # interpolate grid
            x = numpy.arange(0.0, self.xSize, self.xSize/xShape)
            y = numpy.arange(0.0, self.ySize, self.ySize/yShape)
            f = scipy.interpolate.interp2d(x, y, material[key].transpose(), kind='cubic')

            # fill grids
            self.oddGrid[key] = numpy.zeros( (self.xSize/self.deltaX, self.ySize/self.deltaY) )
            self.evenGridX[key] = numpy.zeros( (self.xSize/self.deltaX+1, self.ySize/self.deltaY+1) )
            self.evenGridY[key] = numpy.zeros( (self.xSize/self.deltaX+1, self.ySize/self.deltaY+1) )
            for i in range(0, int(self.xSize/self.deltaX), 1):
                for j in range(0, int(self.ySize/self.deltaY), 1):
                    self.oddGrid[key][i, j] = f(i*self.deltaX, j*self.deltaY)
                    self.evenGridX[key][i, j] = f(i*self.deltaX, (j-0.5)*self.deltaY)
                    self.evenGridY[key][i, j] = f((i-0.5)*self.deltaX, j*self.deltaY)
