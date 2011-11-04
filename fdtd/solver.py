import numpy
from constants import constants
from material import material
import grid as gr

class solver:
    """Solves FDTD equations on given grid, with given materials and ports"""
    def __init__(self, grid, material, mode='TMz', ports=None):
        # save arguments
        self.grid = grid
        self.material = material
        self.mode = mode
        self.ports = ports

        # create memory grid
        self.memoryGrid = gr.grid(self.grid.xSize, self.grid.ySize, self.grid.deltaX, self.grid.deltaY)

    def iterate(self, deltaT, time):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/(self.grid.deltaX*constants.permit)
        c2 = -deltaT/(self.grid.deltaY*constants.permit)
        c3 = deltaT/(self.grid.deltaX*constants.permea)
        c4 = -deltaT/(self.grid.deltaY*constants.permea)

        # swap constants if neccessary
        if self.mode == 'TEz':
            c1, c2, c3, c4 = -c3, -c4, -c1, -c2

        # iterate
        for t in numpy.arange(0.0, time, deltaT):
            # update ports
            for port in self.ports:
                port.update(self.grid, t)

            # calc odd Grid
            xshape, yshape = self.grid.oddGrid.shape
            for x in range(0, xshape, 1):
                for y in range(0, yshape, 1):
                    self.grid.oddGrid[x, y] += c1*(self.grid.evenGridY[x+1, y] - self.grid.evenGridY[x, y]) + c2*(self.grid.evenGridX[x, y+1] - self.grid.evenGridX[x, y])

            # calc even Grid
            for x in range(0, xshape, 1):
                for y in range(1, yshape, 1):
                    self.grid.evenGridX[x, y] += c4*(self.grid.oddGrid[x, y] - self.grid.oddGrid[x, y-1])

            for x in range(1, xshape, 1):
                for y in range(0, yshape, 1):
                    self.grid.evenGridY[x, y] += c3*(self.grid.oddGrid[x, y] - self.grid.oddGrid[x-1, y])

            # print a dot every 100 steps
            if t/deltaT % 100 == 0:
                print '.',
