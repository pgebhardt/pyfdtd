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

    def iterate(self, deltaT, time, starttime=0.0):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/self.grid.deltaX
        c2 = deltaT/self.grid.deltaY
        c3 = constants.permit
        c4 = constants.permea

        # apply mode
        if self.mode == 'TMz':
            m1 = self.material.oddGrid['epsilon']
            m2 = self.material.oddGrid['sigma']
            m3 = self.material.evenGridX['mu']
            m4 = self.material.evenGridY['mu']
            m5 = numpy.zeros(self.material.oddGrid['sigma'].shape)
            m6 = numpy.zeros(self.material.oddGrid['sigma'].shape)
        elif self.mode == 'TEz':
            c1, c2, c3, c4 = -c1, -c2, c4, c3
            m1 = self.material.oddGrid['mu']
            m2 = numpy.zeros(self.material.oddGrid['sigma'].shape)
            m3 = self.material.evenGridX['epsilon']
            m4 = self.material.evenGridY['epsilon']
            m5 = self.material.evenGridX['sigma']
            m6 = self.material.evenGridY['sigma']
        else:
            raise ArgumentError

        # iterate
        for t in numpy.arange(starttime, time, deltaT):
            # update ports
            for port in self.ports:
                port.update(self.grid, t)

            # calc odd Grid
            xshape, yshape = self.grid.oddGrid['field'].shape
            for x in range(1, xshape, 1):
                for y in range(1, yshape, 1):
                    # calc flux density
                    self.grid.oddGrid['flux'][x, y] += c1*(self.grid.evenGridY['field'][x, y] - self.grid.evenGridY['field'][x-1, y]) 
                    self.grid.oddGrid['flux'][x, y] -= c2*(self.grid.evenGridX['field'][x, y] - self.grid.evenGridX['field'][x, y-1])

                    # calc field
                    self.grid.oddGrid['field'][x, y] = (1.0/(c3*m1[x, y] + m2[x, y]))*(self.grid.oddGrid['flux'][x, y] - self.memoryGrid.oddGrid['flux'][x, y])

                    # integrate field
                    self.memoryGrid.oddGrid['flux'][x, y] += m2[x, y]*self.grid.oddGrid['field'][x, y]

            # calc even Grid
            for x in range(0, xshape, 1):
                for y in range(0, yshape-1, 1):
                    # calc flux density
                    self.grid.evenGridX['flux'][x, y] -= c2*(self.grid.oddGrid['field'][x, y+1] - self.grid.oddGrid['field'][x, y])

                    # calc field
                    self.grid.evenGridX['field'][x, y] = (1.0/(c4*m3[x, y] + m5[x, y]))*(self.grid.evenGridX['flux'][x, y] - self.memoryGrid.evenGridX['flux'][x, y])

                    # integrate field
                    self.memoryGrid.evenGridX['flux'][x, y] += m5[x, y]*self.grid.evenGridX['field'][x, y]

            for x in range(0, xshape-1, 1):
                for y in range(0, yshape, 1):
                    # calc flux density
                    self.grid.evenGridY['flux'][x, y] += c1*(self.grid.oddGrid['field'][x+1, y] - self.grid.oddGrid['field'][x, y])

                    # calc field
                    self.grid.evenGridY['field'][x, y] = (1.0/(c4*m4[x, y] + m6[x, y]))*(self.grid.evenGridY['flux'][x, y] - self.memoryGrid.evenGridY['flux'][x, y])

                    # integrate field
                    self.memoryGrid.evenGridY['flux'][x, y] += m6[x, y]*self.grid.evenGridY['field'][x, y]

            if t/deltaT % 100 == 0:
                print "{}%".format((t-starttime)*100/time)
