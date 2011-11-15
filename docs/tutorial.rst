========
Tutorial
========

Creating a simple FDTD
=======================

Probably the first step in using an FDTD is to create the calculation domain.
For an 0.2m x 1.0m domain with a discretization of 1mm it's as simple as this::

   field = fdtd.field(0.2, 1.0, deltaX=0.001)

The second step is to initialize the solver::

   solver = fdtd.solver(field)

With this simple configuration the solver initializes the domain with a PML
boundary condition, no listening or source ports and in TMz mode.

Adding a sources
================

To add a source to our domain we first need a function to discribe the field.
In this example we use a sinoudial modulated gaussian pulse::

   def source_function(t):
   	return math.exp(-(t-300e-12)**2/(2.0*200.0e-12**2))*math.cos(2.0*math.pi*20e9*(t-300e-12))

After that we create a port using this sourcefunction in the middle of our domain
and add it to our solver::

   source = fdtd.port((0.1, 0.1), function=source_function)
   solver.ports.append(source)

Adding a listener
=================

To have a look on what is happening in our calculation domain, we can either watch
the field located at our source or we create a listening port. The only difference
to a source port is the missing sourcefunction::

   listener = fdtd.port((0.1, 0.5))
   solver.ports.append(listener) 

Define material
===============

Defining some material constants is done with slicing. Pyfdtd defines 'epsilon', 'mu' and 'sigma'
material constants. To define e.g. a 10cm x 1cm block of coper in our domain we just have to adjust
the sigma parameter::

   material = solver.material
   material['sigma',0.05:0.15,0.3:0.4] = 59.1e6

Solving
=======

Now it is time to do some solving. Easiest way is to solve for a specific duration::

   solver.solve(10e-9)

This solves the equations for 10ns and of cause applies our specified source and
saves the field information in our listener port. For example to plot the field
at the listener port with matplotlib do as following::

   pyplot.plot(listener.values)
