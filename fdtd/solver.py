import numpy
from constants import constants
from grid import grid
from material import material

class solver:
    """Solves FDTD equations on given grid, with given materials and ports"""
    def __init__(self, grid, material, mode='TMz', ports=None):
        # save arguments
        self.grid = grid
        self.material = material
        self.mode = mode
        self.ports = ports

    def iterate(self, deltaT, timesteps):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/(self.grid.deltaX*constants.permit)
        c2 = deltaT/(self.grid.deltaY*constants.permit)
        c3 = deltaT/(self.grid.deltaX*constants.permea)
        c4 = deltaT/(self.grid.deltaY*constants.permea)

        # swap constants im neccessary
        if self.mode == 'TEz':
            c1, c2, c3, c4 = c3, c4, c1, c2

        # iterate
        for i in range(0, timesteps, 1):
            # calc odd Grid
            xshape, yshape = self.grid.oddGrid.shape
            for x in range(0, xshape, 1):
                for y in range(0, yshape, 1):
                    self.grid.oddGrid[x, y] += c1*(self.grid.evenGridY[x+1, y] - self.grid.evenGridY[x, y]) - c2*(self.grid.evenGridX[x, y+1] - self.grid.evenGridX[x, y])
