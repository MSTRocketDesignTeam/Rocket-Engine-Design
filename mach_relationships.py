import math
from math import pi
import numpy as np
import sympy.solvers
import sympy as sym


def mach_relationships(pointx, pointy, t_t, t_p, y):
    miny_ind = np.where(pointy == np.amin(pointy))  # Outputs a tuple
    miny_ind = miny_ind[0][0]

    areas = area(pointy)
    print(areas[miny_ind - 5], areas[miny_ind], y)
    mach_x_axis(pointx, areas, y, miny_ind)


def area(pointy):
    areas = pi * (pointy ** 2)
    return areas


def mach_x_axis(pointx, areas, y, low):
    my, ay = sym.symbols('my, ay')



    eq = sym.Eq((1 / my) * sym.sqrt(((1 + sym.Pow(my, 2) * (y - 1) / 2) / (1 + (y - 1) / 2)) ** ((y + 1) / (y - 1))) - (areas[low-5] / areas[low]), my)
    print("Ay = ", areas[low-5])
    print("Ax = ", areas[low])
    print("k - ", y)
    print("Mx = ", 1)

    eq1 = Diff

    #eq_dy = sym.diff(eq, my)

    print(eq)
    #print(eq_dy)
    print('done')
