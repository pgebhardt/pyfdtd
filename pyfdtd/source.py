import numpy

class source:
    @staticmethod
    def currentdensity(function):
        """Decorator to create a valid sourcefunction"""
        def res(flux, deltaT, t):
            return -0.5*deltaT*function(t)

        # return sourcefunction
        return res

    @staticmethod
    def fluxdensity(function):
        """ """
        def res(flux, deltaT, t):
            return -0.5*(function(t)-function(t-deltaT))

        # return sourcefunction
        return res
