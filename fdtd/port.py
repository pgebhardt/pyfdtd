import numpy
from field import field
from constants import constants

class port:
    """I/O Port to connect Grids to outer world"""
    def __init__(self, position, function=None):
        # save arguments
        self.position = position
        self.function = function
        self.values = []

    def update(self, field, t=0.0, mode='TMz'):
        """Updates data port and connected grid"""
        x, y = self.position
        x, y = int(x/field.deltaX), int(y/field.deltaY)

        # apply function
        if self.function:
            f = self.function(t)
                 
            if mode == 'TMz':
                field.oddFieldX['flux'][x, y] += 0.5*constants.permit*f
                field.oddFieldY['flux'][x, y] += 0.5*constants.permit*f
            elif mode == 'TEz':
                field.oddFieldX['flux'][x, y] += 0.5*constants.permea*f
                field.oddFieldY['flux'][x, y] += 0.5*constants.permea*f
            else:
                raise AttributeError('mode')

        # get result value
        value = field.oddFieldX['field'][x, y] + field.oddFieldY['field'][x, y]
        self.values.append(value)
