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

__kernel void apply(__global double* field, __global const double* func, __global const double* mask)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] =   mask[x*y_size + y] * func[x*y_size + y] +
                            (1.0 - mask[x*y_size + y]) * field[x*y_size + y];
}

__kernel void zero(__global double* input)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    input[x*y_size + y] = 0.0;
}

__kernel void set(__global double* dest, __global const double* src)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    dest[x*y_size + y] = src[x*y_size + y];
}

__kernel void epsilon(__global double* field, __global const double* flux,
                        __global double* integrate, double er,
                        double sigma, double dt, double t, double e_0)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] = (1.0 / (e_0 * er + sigma * dt)) *
                            (flux[x*y_size + y] - integrate[x*y_size + y]);
    integrate[x*y_size + y] += sigma * field[x*y_size + y] * dt;
}

__kernel void epsilon_with_arrays(__global double* field, __global const double* flux,
                        __global double* integrate, __global const double* er,
                        __global const double* sigma, double dt, double t, double e_0)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] = (1.0 / (e_0 * er[x*y_size + y] + sigma[x*y_size + y] * dt)) *
                            (flux[x*y_size + y] - integrate[x*y_size + y]);
    integrate[x*y_size + y] += sigma[x*y_size + y] * field[x*y_size + y] * dt;
}

__kernel void mu(__global double* field, __global const double* flux,
                        __global double* integrate, double mur,
                        double sigma, double dt, double t, double mu_0)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] = (1.0 / (mu_0 * mur + sigma * dt)) *
                            (flux[x*y_size + y] - integrate[x*y_size + y]);
    integrate[x*y_size + y] += sigma * field[x*y_size + y] * dt;
}

__kernel void mu_with_arrays(__global double* field, __global const double* flux,
                        __global double* integrate, __global const double* mur,
                        __global const double* sigma, double dt, double t, double mu_0)
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    int y_size = get_global_size(1);

    field[x*y_size + y] = (1.0 / (mu_0 * mur[x*y_size + y] + sigma[x*y_size + y] * dt)) *
                            (flux[x*y_size + y] - integrate[x*y_size + y]);
    integrate[x*y_size + y] += sigma[x*y_size + y] * field[x*y_size + y] * dt;
}
