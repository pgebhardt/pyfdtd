import numpy
from grid import grid

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position):
        # save arguments
        self.position = position

    def update(self, grid, value=0.0, mode='append'):
        """Updates data port and connected grid"""
        
        # get result value
        x, y = self.position
        x, y = int(x/grid.deltaX), int(y/grid.deltaY)
        result = grid.evenGrid[x, y]

        # apply value change
        if mode == 'append':
            grid.evenGrid[x, y] += value
        elif mode == 'set':
            grid.evenGrid[x, y] = value
        else:
            raise AttributeError('mode')
            
        # return value
        return result
