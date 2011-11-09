import numpy
from field import field
from constants import constants

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position, messureWave='incoming', function=None):
        # save arguments
        self.position = position
        self.function = function
        self.messureWave = messureWave
        self.values = []

    def update(self, field, t=0.0, mode='TMz'):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/field.deltaX), int(y/field.deltaY)
    
        # check mode
        c = constants.e0
        if mode == 'TEz':
            c = constants.u0

        # apply function
        f = 0.0
        if self.function:
            f = self.function(t)                 
            field.oddFieldX['flux'][x, y] += 0.5*c*f
            field.oddFieldY['flux'][x, y] += 0.5*c*f

        # get result value
        value = field.oddFieldX['field'][x, y] + field.oddFieldY['field'][x, y]
        self.values.append(value)
