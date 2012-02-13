# pyfdtd is a simple 2d fdtd using numpy
# Copyright (C) 2012  Patrik Gebhardt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import math


class constants:
    """Defines neccessary constants"""
    c0 = 2.99792458e8  # m/s
    mu0 = 4.0 * math.pi * 1.0e-7  # Vs/Am
    e0 = 1.0 / (mu0 * c0 ** 2)  # As/Vm

if __name__ == '__main__':
    print 'C0: {}'.format(constants.c0)
    print 'MU0: {}'.format(constants.mu0)
    print 'E0: {}'.format(constants.e0)
