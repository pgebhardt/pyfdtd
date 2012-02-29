# GUI for pyfdtd using PySide
# Copyright (C) 2012  Patrik Gebhardt
# Contact: grosser.knuff@googlemail.com
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


from types import FunctionType
from scipy import constants
from numpy import *


def source_from_string(expression, functions={}):
    # standart pulse function
    def pulse(amplitude=1e3, width=200e-12, freq=20e9, offset=1e-9):
        def res(queue, program, flux, field, deltaT, t, mem):
            value = amplitude * exp(-(t - offset) ** 2 / (2 * width ** 2)) * \
                    cos(2 * pi * freq * (t - offset))

            program.set(queue, field.shape, None, field.data,
                (0.0 * flux + -0.5 * deltaT * value).data)
        return res

    # add pulse to functions
    functions['pulse'] = pulse

    # try parse standart function
    function = eval(expression, functions)

    # check for function type
    if isinstance(function, FunctionType):
        return function

    # if not a source function, create one
    def res(queue, program, flux, field, deltaT, t, mem):
        field = 0.0 * flux + -0.5 * deltaT * eval(expression)

    return res


def material_from_string(expression, functions={}):
    # try parse standart functions
    function = eval(expression, functions)

    # check for function type
    if isinstance(function, FunctionType):
        return function

    # if not a material function, create one
    def res(flux, deltaT, t, mem):
        return eval(expression)

    return res
