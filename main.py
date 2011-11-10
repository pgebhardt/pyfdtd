import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import fdtd

# create listen ports
portlist = []

# add source port
def f(t):
    x = t - 300e-12
    if x < 0.0:
        return math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    elif x < 600e-12:
        return math.cos(2.0*math.pi*40e9*x)
    else:
        return math.exp(-(x-600e-12)**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*40e9*x)
    
portlist.append(fdtd.port((0.1, 0.1), function=f))

# create solver
solver = fdtd.solver(fdtd.field(0.20, 0.20, 0.0005, 0.0005), ports=portlist)

# add material
layer = solver.material.empty_layer()

for i in range(0, 320, 1):
    for j in range(0, 20, 1):
        layer['sigma'][40+i, 360+j] = 59.1e6

solver.material.add_layer(layer)

# iterate
history = solver.iterate(2000e-12, safeHistory=True, historyInterval=5e-12)
print max(portlist[0].values)

# show plot
fig = plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(portlist[0].values)

plt.subplot(2, 1, 2)
ims = []
for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-0.01, 0.01))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=50)

plt.show()
