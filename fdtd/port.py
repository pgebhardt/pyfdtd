import numpy
from grid import grid

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position):
        # save arguments
        self.position = position
        self.values = []

    def update(self, grid, value=0.0, mode='append'):
        """Updates data port and connected grid"""
        
        # get result value
        x, y = self.position
        x, y = int(x/grid.deltaX), int(y/grid.deltaY)
        self.values.append([grid.oddGrid[x, y]])

        # apply value change
        if mode == 'append':
            grid.oddGrid[x, y] += value
        elif mode == 'set':
            grid.oddGrid[x, y] = value
        else:
            raise AttributeError('mode')
