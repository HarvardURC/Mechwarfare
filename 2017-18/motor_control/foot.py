import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from math import pow

t = 0
step = 0.01

homex, homey, homez = 3, -3, 1
endx, endy, endz = homex, homey, homez
x, y, z = homex, homey, 0

vx, vy, vz = 5, 0, 0
ω = 1

xpoints = []
ypoints = []
zpoints = []

beats = 4
beatlen = 1;

while t < (beats * beatlen):
    if 2.0 < (t / beatlen) % 4 < 2.02:
        vx = 0
        vy = 2
    if (t / beatlen) % 4 < 3:
        xpoints.append(x)
        ypoints.append(y)
        zpoints.append(z)
        x += (-vx + y*ω) * step
        y += (-vy - x*ω) * step
    else:
        if endx == homex:
            endx = x
            endy = y
            endz = z
        xpoints.append(x)
        ypoints.append(y)
        zpoints.append(z)
        x += (homex - endx) * (step / beatlen)
        y += (homey - endy) * (step / beatlen)
        if (t % beatlen)/beatlen < 1/4:
            z += (homez - endz) * (step / (beatlen / 4))
        if (t % beatlen)/beatlen > 3/4:
            z -= (homez - endz) * (step / (beatlen / 4))
    t += step

colors = cm.rainbow(np.linspace(0, 1, len(xpoints)))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs=xpoints, ys=ypoints, zs=zpoints, c=colors)
plt.show()
