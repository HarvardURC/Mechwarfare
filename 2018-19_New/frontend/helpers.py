import math as m
import numpy as np

"""
 This file contains:
 rtod(x)
 dtor(x)
 tocyl(point)
 fromcyl(point)
 torad(point)
 fromrad(point)
 bound(x, lower, upper)
 degreesmod(theta)
 dict_timer(key, d, val)
"""

# rtod(x: number in radians)
#   converts x from radians to degrees
def rtod(x):
    return (x * 180 / m.pi)

# dtor(x: number in degrees)
#   converts x from degrees to radians
def dtor(x):
    return (x * m.pi / 180)

# tocyl(point: np.array of 3d cartesian coordinates)
#   converts point from cartesian to cylindrical
def tocyl(point):
    return np.array([rtod(m.atan2(point[1], point[0])), ((point[0]**2 + point[1]**2) ** .5), point[2]])

# fromcyl(point: np.array of cylindrical coordinates)
#   converts point from cylindrical to cartesian)
def fromcyl(point):
    return np.array([point[1] * m.cos(dtor(point[0])), point[1] * m.sin(dtor(point[0])), point[2]])

# torad(point: np.array of 2d cartesian coordinates)
#   converts from cartesian to radial
def torad(point):
    return np.array([rtod(m.atan2(point[1], point[0])), ((point[0]**2 + point[1]**2) ** .5)])

# fromrad(point: np.array of radial coordinates)
#   converts to cylindrical coordinates
def fromrad(point):
    return np.array([point[1] * m.cos(dtor(point[0])), point[1] * m.sin(dtor(point[0]))])

# bound(x, lower, upper)
#   bounds x 
def bound(x, lower, upper):
	return (min(max(x, lower), upper))

# degreesmod(theta)
#   ensures 0 <= theta < 360 (uses degrees)
def degreesmod(theta):
	while(theta < 0):
		theta = theta + 360
	return (theta % 360)

# dict_timer(key, d, val)
#   aggregates times in dict
def dict_timer(key, d, val):
    if (key in d):
        d[key] += val
    else:
        d[key] = val
    return d
