#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate the magnetic field from a arbitrary current loop.

Author: Carlos Galdino
Email: galdino@ifi.unicamp.br
"""

import numpy as np
from scipy.special import ellipk, ellipe


def b_field(r, r0, n, radius, current):
    """Return the magnetic field from an arbitrary current loop.

    See eqns (1) and (2) in Phys Rev A Vol. 35, N 4, pp. 1535-1546; 1987.

    Parameters
    ----------
    r : list [x y z]
        Position vector where the magnetc field is to be evaluated,
         where x, y, z in meters.
    n: list [x y z]
        Normal vector of loop plane at its center.
        Current I is oriented by the right-hand-rule.
    r0 : list [x y z]
        Position vector of the loop center, where x, y, z in meters.
    R : float
        Radius of the loop in meters.

    Returns
    -------
    numpy array [x y z]
    Magnetic field vector at point r in Tesla.

    """
    n = np.array(n)
    n = n / np.sqrt(sum(n*n))  # normalize n

    # choose two vectors perpendicular to n
    # choice is arbitrary since the coil is symetric about n
    if abs(n[1]) == 1:
        l = [n[2], 0, -n[0]]
    else:
        l = [0, n[2], -n[1]]
    l = np.array(l)
    l = l / np.sqrt(sum(l*l))  # normalize n

    m = np.cross(n, l)

    trans = np.array([l.transpose(), m.transpose(), n.transpose()]) # transformation matrix coil frame to lab frame
    invTrans = np.linalg.inv(trans)

    r1 = np.array(r) - np.array(r0)  # point location from center of coil
    r2 = np.matmul(invTrans, r1.transpose())  #transform vector to coil frame

    # Calculate field
    x = r2[0]
    y = r2[1]
    z = r2[2]
    rho = np.sqrt(x**2 + y**2)

    if rho == 0 and z == 0:
        Bz = 0
        Brho = 0
        co = 0
        si = 0
    else:
        k_1 = np.sqrt((4 * radius * rho) / ((radius + rho)**2 + z**2))
        k = ellipk(k_1**2)
        e = ellipe(k_1**2)
        Bz = (1 / np.sqrt((radius + rho) ** 2 + z ** 2)) * (k + e *
                                                          (radius ** 2 - rho ** 2 - z ** 2) / ((radius - rho) ** 2 + z ** 2))
        if rho == 0:
            Brho = 0
            co = 0
            si = 0
        else:
            Brho = (z / (rho * np.sqrt((radius + rho) ** 2 + z ** 2))) * (
                        -k + e * (radius ** 2 + rho ** 2 + z ** 2) / ((radius - rho) ** 2 + z ** 2))
            co = (x / np.sqrt(x ** 2 + y ** 2))
            si = (y / np.sqrt(x ** 2 + y ** 2))
    field_b = np.array([co * Brho, si * Brho, Bz])
    return np.matmul(trans, field_b.transpose()) * current * 2e-7


if __name__ == '__main__':
    print(b_field([-0.2, -5.551115123125783e-17, 0.0], [0, 0, 0.05], [0, 0, 1], 0.2, 1))
