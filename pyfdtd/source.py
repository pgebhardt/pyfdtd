class source:
    @staticmethod
    def currentdesity(function):
        """Decorator to create a valid sourcefunction"""
        def res(flux, deltaT, t):
            return -0.5*deltaT*function(t-0.5*deltaT)

        # return sourcefunction
        return res

    @staticmethod
    def fieldstrength(function):
        """ """
        def res(flux, deltaT, t):
            pass
        
        # return sourcefunction
        return res
