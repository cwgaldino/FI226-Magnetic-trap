#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:21:48 2019.

@author: galdino
"""


from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import filemanip as file
from arraymanip import increasing_monotonicity

try: %matplotlib qt5
except: pass

# %% Bz
plt.figure()
data = np.genfromtxt(str('z_simi_exact.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Perfect coil simulation')
data = np.genfromtxt(str('z_simi_real.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Square-packing coil simulation')
data = np.loadtxt(str('Medida_Z_Geral.csv'), skiprows=1)
plt.plot(data[:, 0]-35, data[:, 1], marker='o', linewidth=0, label='Measured')
plt.xlabel('z (mm)')
plt.ylabel('Bz (G)')
plt.legend()
plt.savefig('Bz.svg')

# %% Raw Bz derivative
plt.figure()
data = np.genfromtxt(str('z_der_simi_exact.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Perfect coil simulation')
data = np.genfromtxt(str('z_der_simi_real.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Square-packing coil simulation')
data = np.loadtxt(str('Medida_Z_Geral.csv'), skiprows=1)
plt.plot(data[:-1, 0]-35, -np.diff(data[:, 1])/np.diff(data[:, 0]) * 10, marker='o', linewidth=0, label='Measured')
plt.xlabel('z (mm)')
plt.ylabel('dBz/dz (G/cm)')
plt.legend(loc='lower right')
plt.savefig('dBz_raw.svg')

# %% spline Bz
from scipy.interpolate import interp1d
data = file.getDataDict('medida_z_ordered.dat')
x = np.linspace(-35, 30, 1000)
y = interp1d(data['z(mm)'], data['Bz(G)'], kind='cubic')
y_mean = []
x_mean = []
for i in np.arange(0,1000,20):
    y_mean.append(np.mean(y(x)[i:i+100]))
    x_mean.append(np.mean(x[i:i+100]))
plt.plot(x, y(x), marker='o', linewidth=0, label='Interpolated Bz data')
plt.plot(x_mean, y_mean, marker='o', linewidth=0, label='Average each 100 points')
plt.xlabel('z (mm)')
plt.ylabel('Bz (G)')
plt.legend()
plt.savefig('Bz_interp.svg')

# %% dBz from interpolated data
data = np.genfromtxt(str('z_der_simi_real.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Square-packing coil simulation')
plt.plot(x_mean[:-1], -np.diff(y_mean)/np.diff(x_mean) *10, marker='o', linewidth=0, label='Derivative of average data')
plt.xlabel('z (mm)')
plt.ylabel('dBz/dz (G/cm)')
plt.legend(loc='lower right')
plt.savefig('dBz_interp.svg')

# %% fit Bz
data = file.getDataDict('medida_z_ordered.dat')
p = np.polyfit(data['z(mm)'], data['Bz(G)'], deg=5)
plt.plot(data['z(mm)'], data['Bz(G)'], marker='o', linewidth=0, label='Measured')
x = np.linspace(-35, 30, 1000)
plt.plot(x, np.poly1d(p)(x), linewidth=1, label='5 order polynomial fit')
plt.xlabel('z (mm)')
plt.ylabel('Bz (G)')
plt.legend()
plt.savefig('Bz_fit.svg')

# %% dBz from fit
data = np.genfromtxt(str('z_der_simi_real.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Square-packing coil simulation')
plt.plot(x[50+1:-50:20]+2, (-np.diff(np.poly1d(p)(x))/np.diff(x) * 10)[50:-50:20], marker='o', linewidth=0, label='Derivative of polynomial fit')
plt.xlabel('z (mm)')
plt.ylabel('dBz/dz (G/cm)')
plt.legend(loc='lower right')
plt.savefig('dBz_fit.svg')
