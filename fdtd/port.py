import numpy
from field import field

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position, function=None):
        # save arguments
        self.position = position
        self.function = function
        self.values = []

    def update(self, field, t=0.0, mode='append'):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/field.deltaX), int(y/field.deltaY)

        # apply function
        if self.function:
            f = self.function(t)
                 
            if mode == 'append':
                field.oddFieldX['flux'][x, y] += 0.5*f
                field.oddFieldY['flux'][x, y] += 0.5*f
            elif mode == 'set':
                field.oddFieldX['flux'][x, y] = 0.5*f
                field.oddFieldY['flux'][x, y] = 0.5*f
            else:
                raise AttributeError('mode')

        # get result value
        self.values.append([field.oddFieldX['flux'][x, y]] + field.oddFieldY['flux'][x, y])
