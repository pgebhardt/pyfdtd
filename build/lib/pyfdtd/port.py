import numpy
from field import field
from constants import constants

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, x, y, function=None):
        # save arguments
        self.position = x, y
        self.function = function
        self.values = []

    def update(self, field, t=0.0):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/field.deltaX), int(y/field.deltaY)
    
        # get result value
        value = field.oddFieldX['field'][x, y] + field.oddFieldY['field'][x, y]
        self.values.append(value)

        # apply function
        f = 0.0
        if self.function:
            f = -self.function(t)
            field.oddFieldX['field'][x, y] += 0.5*f
            field.oddFieldY['field'][x, y] += 0.5*f
