import numpy
import constants as constants
import field as fi

class material:
    """Descripes the material"""
    def __init__(self, xSize, ySize, deltaX, deltaY):
        # init layer
        xShape = xSize/deltaX
        yShape = ySize/deltaY
        self.layerlist = [ {'epsilon': numpy.ones((xShape, yShape)), 'mu': numpy.ones((xShape, yShape)), 'sigma': numpy.zeros((xShape, yShape)) } ]

        # create memoryField
        self.memoryField = fi.field(xSize, ySize, deltaX, deltaY)

    def add_layer(layer):
        pass

    def get_material(self):
        # cummulate all layers

        # return sum
        return self.layerlist[0]
        
        
