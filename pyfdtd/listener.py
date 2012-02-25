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


class Listener:
    def __init__(self, posX, posY):
        # save attribute
        self.pos = posX, posY

        # create value storage
        self.X, self.Y, self.Z = [], [], []
        self.values = self.X, self.Y, self.Z

    def update(self, field):
        # get value
        x, y, z = field[self.pos]

        # save value
        self.X.append(x)
        self.Y.append(y)
        self.Z.append(z)
