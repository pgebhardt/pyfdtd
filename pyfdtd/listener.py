# pyfdtd is a simple 2d fdtd using numpy
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
from numpy import array


class Listener:
    def __init__(self, posX, posY):
        # save attribute
        self.pos = posX, posY

        # create value
        self.X, self.Y, self.Z = array((1, )), array((1, )), array((1, ))
        self.values = self.X, self.Y, self.Z
        self.clvalues = 0.0

    def copy_to_host(self):
        # get array
        values = self.clvalues.get()

        # split buffer
        self.X = values[:, 0]
        self.Y = values[:, 1]
        self.Z = values[:, 2]

        # set values
        self.values = self.X, self.Y, self.Z
