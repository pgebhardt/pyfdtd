import math
import numpy
import scipy.interpolate
import matplotlib.pyplot as plt
import fdtd

# create listen ports
portlist = []
for i in range(1, 5, 1):
    portlist.append(fdtd.port( (i*0.01, 0.0) ))

# add source port
def f(t):
    x = t - 300e-12
    return math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)

portlist.append(fdtd.port( (0.025, 0.025), f))

# create solver
solver = fdtd.solver(fdtd.grid(0.05, 0.05, 0.001, 0.001), fdtd.material(0.05, 0.05, 0.001, 0.001), 
    ports=portlist)

# iterate
solver.iterate(1.0e-12, 350e-12)

# plot ports
plt.figure(1)
plt.imshow(solver.grid.oddGrid['flux'])
plt.show()
