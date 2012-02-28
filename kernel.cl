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

#pragma OPENCL EXTENSION cl_hkr_fp64: enable

__kernel void oddFieldX(__global double* oddFieldX, __global double* evenFieldX, double ky)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1) + 1;

    oddFieldX[x*y_size + y] -= ky * (evenFieldX[x*y_size + y+1] - evenFieldX[x*y_size + y]);
}

__kernel void oddFieldY(__global double* oddFieldY, __global double* evenFieldY, double kx)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1) + 1;

    oddFieldY[x*y_size + y] += kx * (evenFieldY[(x+1)*y_size + y] - evenFieldY[x*y_size + y]);
}
