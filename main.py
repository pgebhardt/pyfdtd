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

def mat(x, y):
    if (x - 0.2)**2 + (y - 0.2)**2 > 0.1**2:
        return 59.1e6

    else:
        return 0.0
        
portlist.append(pyfdtd.port((0.2, 0.2), function=f))

# create solver
solver = pyfdtd.solver(pyfdtd.field(0.4, 0.4, deltaX=0.001), ports=portlist)

# add material
solver.material['sigma'] = mat

# iterate
history = solver.solve(5e-9, saveHistory=True)

# show plot
fig = plt.figure(1)
#plt.subplot(2, 1, 1)
#plt.plot(portlist[0].values)

#plt.subplot(2, 1, 2)
ims = []
for f in history:
    im = plt.imshow(f, norm=colors.Normalize(-0.01, 0.01))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=20)

plt.show()
