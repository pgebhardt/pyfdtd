import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import pyfdtd

# create listen ports
portlist = []

# add source port
def f(t):
    x = t - 1000e-12
    return math.exp(-x**2/(2.0*200.0e-12**2))*math.cos(2.0*math.pi*20e9*x)
    
portlist.append(pyfdtd.port((0.1, 0.1), function=f))

# create solver
solver = pyfdtd.solver(pyfdtd.field(0.20, 0.40, deltaX=0.001), ports=portlist)

# add material
layer = solver.material.empty_layer()
layer['sigma'][:,360:] = 59.1e6
solver.material.add_layer(layer)

# iterate
history = solver.iterate(3000e-12, safeHistory=True)

# show plot
fig = plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(portlist[0].values)

plt.subplot(2, 1, 2)
ims = []
for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-0.01, 0.01))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=20)

plt.show()
