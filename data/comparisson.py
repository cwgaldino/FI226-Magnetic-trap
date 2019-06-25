#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:21:48 2019.

@author: galdino
"""


from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("/home/galdino/github/myModules")
import filemanip as file
from arraymanip import increasing_monotonicity

%matplotlib qt5

# %% Ordering data
data = np.loadtxt(str('Medida_Z_Geral.csv'), skiprows=1)
x = np.linspace(-35, 30, 1000)
x_data, y_data = increasing_monotonicity(data[:, 0]-35, data[:,1])
temp = {'z(mm)':x_data, 'Bz(G)':y_data}
file.saveDataDict(temp, '.', 'medida_z_ordered.dat')


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


# %% DERIVATIVE
plt.figure()
data = np.genfromtxt(str('z_der_simi_exact.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Perfect coil simulation')
data = np.genfromtxt(str('z_der_simi_real.csv'), skip_header=4, delimiter=',')
plt.plot(-data[:, 0]*1000, data[:, 1], label='Square-packing coil simulation')
data = np.loadtxt(str('Medida_Z_Geral.csv'), skiprows=1)
plt.plot(data[:-1, 0]-35, -np.diff(data[:, 1])/np.diff(data[:, 0]) * 10, marker='o', linewidth=0, label='Measured')
plt.xlabel('z (mm)')
plt.ylabel('dBz/dz (G/cm)')
plt.legend()
plt.savefig('dBz.svg')

# %% interpolated data
plt.figure()
data = np.loadtxt(str('Medida_Z_Geral.csv'), skiprows=1)
x = np.linspace(-35, 30, 1000)
from arraymanip import increasing_monotonicity
x_data, y_data = increasing_monotonicity(data[:, 0]-35, data[:,1])
temp = {'z(mm)':x_data, 'Bz(G)':y_data}
file.saveDataDict(temp, '.', 'medida_z_ordered.dat')
y = np.interp(x, x_data, y_data)
plt.plot(x_data, y_data, marker='o', linewidth=0, label='')
plt.plot(x, y, linewidth=.5, label='')
# %%
plt.figure()
plt.plot(data[:-1, 0]-35, -np.diff(data[:, 1])/np.diff(data[:, 0]) * 10, marker='o', linewidth=0, label='Measured')
plt.plot(data[:-1, 0]-35, -np.diff(data[:, 1])/np.diff(data[:, 0]) * 10, marker='o', linewidth=0, label='Measured')
plt.xlabel('z (mm)')
plt.ylabel('dBz/dz (G/cm)')
plt.legend()
plt.savefig('dBz.svg')
