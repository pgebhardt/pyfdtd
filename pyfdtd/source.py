def source(function):
    """Decorator to create a valid sourcefunction"""
    def res(flux, deltaT, t):
        return -0.5*deltaT*function(t)

    # return sourcefunction
    return res
