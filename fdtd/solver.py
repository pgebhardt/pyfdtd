import numpy
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
        pass
