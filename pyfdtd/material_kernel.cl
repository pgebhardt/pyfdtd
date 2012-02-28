/* pyfdtd is a simple 2d fdtd using numpy
   Copyright (C) 2012  Patrik Gebhardt
   Contact: grosser.knuff@googlemail.com

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>. */

__kernel void apply(__global double* field, __global double* func, __global double* mask)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] =   mask[x*y_size + y] * func[x*y_size + y] +
                            (1.0 - mask[x*y_size + y]) * field[x*y_size + y];
}
