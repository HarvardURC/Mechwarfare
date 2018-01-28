import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from math import pow

t = 0
step = 0.01

homes = [[3, -3, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
ends = [home for home in homes]
coords = [[home[0], home[1], 0] for home in homes]
vs = [[5, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
ωs = [1, 0, 0, 0]

points = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]

beats = 4
beatlen = 1

while t < (beats * beatlen):
    if 2.0 < (t / beatlen) % 4 < 2.02:
        vs[0][0] = 0
        vs[0][1] = 2
    if (t / beatlen) % 4 < 3:
        points[0][0].append(coords[0][0])
        points[0][1].append(coords[0][1])
        points[0][2].append(coords[0][2])
        coords[0][0] += (-vs[0][0] + coords[0][1]*ωs[0]) * step
        coords[0][1] += (-vs[0][1] - coords[0][0]*ωs[0]) * step
    else:
        if ends[0][0] == homes[0][0]:
            ends[0][0] = coords[0][0]
            ends[0][1] = coords[0][1]
            ends[0][2] = coords[0][2]
        points[0][0].append(coords[0][0])
        points[0][1].append(coords[0][1])
        points[0][2].append(coords[0][2])
        coords[0][0] += (homes[0][0] - ends[0][0]) * (step / beatlen)
        coords[0][1] += (homes[0][1] - ends[0][1]) * (step / beatlen)
        if (t % beatlen)/beatlen < 1/4:
            coords[0][2] += (homes[0][2] - ends[0][2]) * (step / (beatlen / 4))
        if (t % beatlen)/beatlen > 3/4:
            coords[0][2] -= (homes[0][2] - ends[0][2]) * (step / (beatlen / 4))
    t += step

colors = cm.rainbow(np.linspace(0, 1, len(points[0][0])))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs=points[0][0], ys=points[0][1], zs=points[0][2], c=colors)
plt.show()
