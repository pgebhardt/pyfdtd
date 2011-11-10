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

    def update(self, field, deltaT, S, t=0.0):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/field.deltaX), int(y/field.deltaY)
    
        # get result value
        value = field.oddFieldX['field'][x, y] + field.oddFieldY['field'][x, y] + 1.075350807*self.function(t-0.64*deltaT)
        self.values.append(value)

        # apply function
        f = 0.0
        if self.function:
            f = 2.0*S*self.function(t-0.5*deltaT)
            field.oddFieldX['field'][x, y] += 0.5*f
            field.oddFieldY['field'][x, y] += 0.5*f
