import math

class constants:
    """Defines neccessary constants"""
    c0 = 2.99792458e8 # m/s
    u0 = 4.0*math.pi*1.0e-7 # Vs/Am
    e0 = 1.0/(u0*c0**2) # As/Vm

if __name__ == '__main__':
    print 'C0: {}'.format(constants.c0)
    print 'U0: {}'.format(constants.u0)
    print 'E0: {}'.format(constants.e0)
