#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate the magnetic field from a arbitrary current loop."""

import numpy as np
from scipy.special import ellipk, ellipe


def field_loop(r, r0, n, R, I):
    """Return the magnetic field from an arbitrary current loop.

    See eqns (1) and (2) in Phys Rev A Vol. 35, N 4, pp. 1535-1546; 1987.

    Parameters
    ----------
    r : list [x y z]
        Position vector where the magnetc field is to be evaluated,
         where x, y, z in meters.
    r0 : list [x y z]
        Position vector of the loop center, where x, y, z in meters.
    n: list [x y z]
        Normal vector of loop plane at its center.
        Current I is oriented by the right-hand-rule.
    R : float
        Radius of the loop in meters.
    I : float
        Electrical current in A.

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

    #calculate field
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
        k_1 = np.sqrt((4 * R * rho) / ((R + rho)**2 + z**2))
        k = ellipk(k_1**2)
        e = ellipe(k_1**2)
        Bz = (1 / np.sqrt((R + rho) ** 2 + z ** 2)) * (k + e *
                                                          (R ** 2 - rho ** 2 - z ** 2) / ((R - rho) ** 2 + z ** 2))
        if rho == 0:
            Brho = 0
            co = 0
            si = 0
        else:
            Brho = (z / (rho * np.sqrt((R + rho) ** 2 + z ** 2))) * (
                        -k + e * (R ** 2 + rho ** 2 + z ** 2) / ((R - rho) ** 2 + z ** 2))
            co = (x / np.sqrt(x ** 2 + y ** 2))
            si = (y / np.sqrt(x ** 2 + y ** 2))
    field_b = np.array([co * Brho, si * Brho, Bz])
    return np.matmul(trans, field_b.transpose()) * I * 2e-7


def field_anti_helmholtz(coil_turns, R, D, I, r):
    """Calculate field inside anti-helmholtz coils.

    Their normal vector points in the z direction.

    First coil is in the position [0, 0, D] and its normal vector n points in
    the +z direction.
    The current direction follows the right hand-rule regarding the normal
    vector.

    :param coil_turns: number of turns in the coil.
    :param R: coil radius in m.
    :param D: distance between the coordinate system and the coils in m.
    :param I: electric current in A.
    :param r: position vector r in the space to evaluate B field

    :return: vector representing B field in position r.

    """

    n_1 = [0, 0, 1]
    r0_1 = [0, 0, abs(D)]
    n_2 = [0, 0, -1]
    r0_2 = [0, 0, -abs(D)]

    field_1 = field_loop(r, r0_1, n_1, R, I)
    field_2 = field_loop(r, r0_2, n_2, R, I)

    return coil_turns * (field_1 + field_2)
