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


from setuptools import setup


setup(
    name='pyfdtd',
    version='0.2.0',
    description='2D FDTD using numpy',
    long_description='pyfdtd is a 2D electromagnetic fieldsolver' + \
            'in time-domain using numpy.',
    author=', '.join((
        'Patrik Gebhardt <grosser.knuff@googlemail.com>',
    )),
    author_email='grosser.knuff@googlemail.com',
    url='http://schansge.github.com/pyfdtd/',
    download_url='http://github.com/schansge/pyfdtd/downloads',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    packages=['pyfdtd'],
)
