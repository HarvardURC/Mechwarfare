import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from math import pow, pi

t = 0
step = 0.01

homes = [[3, -3, 1], [3, 3, 1], [-3, 3, 1], [-3, -3, 1]]
ends = [list(home) for home in homes]
coords = [[home[0], home[1], 0] for home in homes]
vs = [5, 0, 0]
ω = 1
lift_height = 1

points = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]

beats = 12
beatlen = 1

def update_leg(i):
    tphase = t + i*beatlen
    
    # on ground
    if (tphase / beatlen) % 4 < 3:
        points[i][0].append(coords[i][0])
        points[i][1].append(coords[i][1])
        points[i][2].append(coords[i][2])
        coords[i][0] += (-vs[0] + coords[i][1]*ω) * step
        coords[i][1] += (-vs[1] - coords[i][0]*ω) * step
    
    # in air
    else:
        if(-0.01 < tphase % beatlen < 0.01):
            ends[i][0] = coords[i][0]
            ends[i][1] = coords[i][1]
            ends[i][2] = coords[i][2]
        points[i][0].append(coords[i][0])
        points[i][1].append(coords[i][1])
        points[i][2].append(coords[i][2])
        coords[i][0] += (homes[i][0] - ends[i][0]) * step / beatlen
        coords[i][1] += (homes[i][1] - ends[i][1]) * step / beatlen
        
        # lift foot
        if (tphase % beatlen)/beatlen < 1/4:
            coords[i][2] += (homes[i][2]) * (step / (beatlen / 4))
            
        # drop foot
        if (tphase % beatlen)/beatlen > 3/4:
            coords[i][2] -= (homes[i][2]) * (step / (beatlen / 4))

while t < (beats * beatlen):
    update_leg(0)
    if(t > 3*beatlen):
        update_leg(1)
    if(t > 2*beatlen):
        update_leg(2)
    if(t > 1*beatlen):
        update_leg(3)
    t += step

for i in range(len(points)):
    colors = cm.rainbow(np.linspace(0, 1, len(points[i][0])))
    fig = plt.figure()
    a = fig.add_subplot(111, projection='3d')
    a.scatter(xs=points[i][0], ys=points[i][1], zs=points[i][2], c=colors)

plt.interactive(False)
plt.show()
