def source(function):
    """Creates a valid sourcefunction of the given function"""
    def res(flux, deltaT, t).
        return -0.5*deltaT*function(t-0.5*deltaT)

    # return sourcefunction
    return res
