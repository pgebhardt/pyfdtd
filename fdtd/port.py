import numpy
from grid import grid

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position, function=None):
        # save arguments
        self.position = position
        self.function = function
        self.values = []

    def update(self, grid, t=0.0, mode='append'):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/grid.deltaX), int(y/grid.deltaY)

        # apply function
        if self.function:
            f = self.function(t)
                 
            if mode == 'append':
                grid.oddGrid['flux'][x, y] += f
            elif mode == 'set':
                grid.oddGrid['flux'][x, y] = f
            else:
                raise AttributeError('mode')

        # get result value
        self.values.append([grid.oddGrid['flux'][x, y]])
