# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 14:52:28 2019

@author: Carlos
"""

import numpy as np
import scipy.integrate as integrate
from scipy.special import erf


def Gauss(x, A, c, w):
    '''
    Gaussian distribution.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: Sigma (standard deviation)
    :return: Result y(x)
    '''
    return A*np.exp(-(x-c)**2/(2*w**2))


def fwhmGauss(x, A, c, w):
    '''
    Gaussian distribution.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''
    return A*np.exp((-4*np.log(2)*((x-c)**2))/(w**2))


def fwhmAreaGauss(x, A, c, w):
    '''
    Gaussian distribution.

    :param x: x value
    :param A: Area under the curve
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''
    return (A/(w*np.sqrt(np.pi/4*np.log(2))))*np.exp((-4*np.log(2)*((x-c)**2))/(w**2))


def Lorentz(x, A, c):
    '''
    Cauchy–Lorentz distribution.

    :param x: x value
    :param A: Scale factor (gamma)
    :param c: Center
    :return: Result y(x)
    '''
    return (1/(np.pi*A))*((A**2)/(A**2 + (x-c)**2))


def fwhmLorentz(x, A, c, w):
    '''
    Cauchy–Lorentz distribution.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''
    return A*((w**2)/(w**2 +4* (x-c)**2))


def fwhmAreaLorentz(x, a, c, w, offset):
    '''
    Cauchy–Lorentz distribution.

    :param x: x value
    :param A: Area under the curve
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''
    return ((2**A)/(np.pi))*((w)/(w**2 +4*(x-c)**2))


def fwhmVoigt(x, A, c, w, m):
    '''
    Pseudo-voigt curve.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :param m: Factor from 1 to 0 of the lorentzian amount
    :return: Result y(x)
    '''
    lorentz = ((w**2)/(w**2 +4* (x-c)**2))
    gauss = np.exp((-4*np.log(2)*((x-c)**2))/(w**2))

    return A*(m*lorentz + (1-m)*gauss)


def fwhmAreaVoigt(x, A, c, w, m):
    '''
    Pseudo-voigt curve.

    :param x: x value
    :param A: is the Area
    :param c: Center
    :param w: FWHM
    :param m: Factor from 1 to 0 of the lorentzian amount
    :return: Result y(x)
    '''
    lorentz = ((2**A)/(np.pi))*((w)/(w**2 +4*(x-c)**2))
    gauss = (A/(b*np.sqrt(np.pi/4*np.log(2))))*np.exp((-4*np.log(2)*((x-c)**2))/(w**2))

    return A*(m*lorentz + (1-m)*gauss)


def fwhmArctan(x, A, c, w):
    '''
    Arctangent function.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :param m: Factor from 1 to 0 of the lorentzian amount
    :return: Result y(x)
    '''

    return A * np.arctan(w*(x - c)) + A * (np.pi/2)


def fwhmErr_1(x, A, c, w):
    '''
    This error function is the integral of the fwhmGauss().

    I never fully tested this function

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''

    data1 = np.zeros([len(x)])

    for i, val in enumerate(x):

       if val>c: points = [c]
       else: points = None

       y,error = integrate.quad(lambda x: fwhmGauss(x, A, c, w), c-1000*w, val, points=points, limit=10000)
       data1[i] = y

       if error>10**-7:
           print('WARNING! Point x= ', val, ' has error= ', error)

    return data1

def fwhmErr_2(x, A, c, w):
    '''
    This error function is the integral of the fwhmGauss() calculated by scipy.special.erf()

    I never fully tested this function.

    :param x: x value
    :param A: Amplitude
    :param c: Center
    :param w: FWHM
    :return: Result y(x)
    '''
    return A * erf(w*(x - c))
