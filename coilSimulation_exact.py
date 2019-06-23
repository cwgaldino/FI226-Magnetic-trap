#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template to build pyqt application using pyqtgraph's dock widget system.

The dockarea system allows the design of user interfaces which can be
rearranged by the user at runtime. Docks can be moved, resized, stacked, and
torn out of the main window. This is similar in principle to the docking system
built into Qt, but
offers a more deterministic dock placement API (in Qt it is very difficult to
programatically generate complex dock arrangements). Additionally, Qt's docks
are
designed to be used as small panels around the outer edge of a window.
Pyqtgraph's
docks were created with the notion that the entire window (or any portion of
it)
would consist of dockable components.
"""

# %% ############## Imports ########################
import pyqtgraph as pg
# import pyqtgraph.console
from pyqtgraph.dockarea import *
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from functools import partial
import numpy as np
import sys
from coil_utils import field_anti_helmholtz
from pyQtUtils.pyQt_utils import slider_win, setSlider, mySlider


class Window(QtGui.QMainWindow):
    """Temp docstring."""

    def __init__(self):
        """Temp docstring."""
        super().__init__()

        # %% plot parameters
        self.z_min = -10e-2  # m
        self.z_max = 10e-2  # m
        self.n_points = 100  # number of points to evaluate field within z_min and z_max
        if self.z_max>self.z_min:
            self.z_array = np.linspace(self.z_min, self.z_max, self.n_points)
        else:
            raise ValueError('z_max must be bigger than z_min')
        # pre-allocate Bz
        self.Bz = np.ones(self.n_points)

        # %% ########### variables parameters ########################
        # parameter table 1
        self.variables      = dict(T=150, R=2.5e-2, D=4.9e-2/2, I=1)
        self.variables_min  = dict(T=1,   R=0.5e-2, D=0,        I=0)
        self.variables_max  = dict(T=500, R=10e-2,  D=10e-2,      I=10)
        self.variables_step = dict(T=1,   R=.1e-2,  D=.1e-2/2, I=.5)
        self.variables_txt = dict(T='(turns)',   R='(m)',  D='(m)', I='(A)')
        self.table1 = list(self.variables.keys())

        # %% ########## window parameters ############
        self.resize(1000, 800)
        self.setWindowTitle('FI226 - Coil Simulation (exact)')

        # %% ########## Init dockable area ###############
        self.area = DockArea()
        self.setCentralWidget(self.area)

        # %% ################ Create and place docks ##################
        self.d1 = Dock("Magnetic field in the z direction Bz for x=0 and y=0", size=(1, 1), closable=True)
        self.d2 = Dock("Derivative of Bz with respect to z", size=(1, 1), closable=True)
        self.d3 = Dock("parameter table", size=(1, 1))

        self.area.addDock(self.d1, 'left')
        # self.area.addDock(self.d1, 'above', self.d6)
        self.area.addDock(self.d2, 'right')

        self.area.addDock(self.d3, 'bottom')

        # Move docks programatically after they have been placed
        # self.area.moveDock(self.d4, 'top', self.d2)  # move d4 to top edge of d2

        # %% #################### dock 1 ########################
        self.w1 = pg.LayoutWidget()
        # self.d1.hideTitleBar()
        # Add (and set) a plot into this dock
        self.w1 = pg.PlotWidget(title=None)
        self.w1.setLabel('bottom', text='z position', units='m')
        self.w1.setLabel('left', text='Bz', units='G')
        self.curve_plot1_1 = self.w1.plot([], pen='g')
        self.curve_plot1_2 = self.w1.plot([], pen='r')
        self.d1.addWidget(self.w1)

        # %% #################### dock 2 ########################
        self.w2 = pg.LayoutWidget()
        # self.d1.hideTitleBar()
        # Add (and set) a plot into this dock
        self.w2 = pg.PlotWidget(title=None)
        self.w2.setLabel('bottom', text='z position', units='m')
        self.w2.setLabel('left', text='dBz/dz', units='G/cm')
        self.curve_plot2_1 = self.w2.plot([], symbolBrush=None, pen='y')
        self.curve_plot2_2 = self.w2.plot([], pen='g')
        self.d2.addWidget(self.w2)

        # %% #################### dock 3 ########################
        # This is a parameter dock.
        self.sliders = dict()
        for idx, variable in enumerate(self.table1):
            value = self.variables[variable]
            min   = self.variables_min[variable]
            max   = self.variables_max[variable]
            step  = self.variables_step[variable]
            txt   = self.variables_txt[variable]
            self.sliders[variable] = self.createSlider(variable, min, max, step, value, txt)

            self.d3.addWidget(self.sliders[variable]['btn'],    row=idx, col=1)
            self.d3.addWidget(self.sliders[variable]['slider'], row=idx, col=2)
            self.d3.addWidget(self.sliders[variable]['txt'],    row=idx, col=3)
            self.d3.addWidget(self.sliders[variable]['lineEdit'], row=idx, col=4)

        # %% ################### act ############################
        self.update()
        self.show()

    def createSlider(self, variable, min, max, step, value, extra_text=None):
        """Fast slider creation.

        It creates all the labels and a settings button for your slider.
        """
        slider = dict()

        slider['btn'] = QtGui.QPushButton('Set')
        slider['btn'].setFixedWidth(40)

        slider['slider'] = mySlider(QtCore.Qt.Horizontal, self)
        slider['slider'].setStep(step)
        slider['slider'].setMaximum(max)
        slider['slider'].setMinimum(min)
        slider['slider'].setValue(value)

        if extra_text is None:
            slider['txt'] = QtGui.QLabel(variable)
        else:
            slider['txt'] = QtGui.QLabel(variable+''+extra_text)
        slider['txt'].setContentsMargins(20, 0, 0, 0)

        slider['lineEdit'] = QtGui.QLineEdit(self)
        slider['lineEdit'].setFixedWidth(100)
        slider['lineEdit'].setContentsMargins(20, 0, 20, 0)
        slider['lineEdit'].setText('{0}'.format(value))
        # slider['lineEdit'].setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Connect
        slider['btn'].clicked.connect(partial(self.openSliderWindow, slider['slider']))
        slider['lineEdit'].editingFinished.connect(partial(self.update_from_text, variable, slider['lineEdit'], slider['slider']))  # Edit this
        slider['slider'].valueChanged.connect(partial(self.update_from_slider, variable, slider['slider'], slider['lineEdit']))  # Edit this

        return slider

    def update_from_text(self, variable, lineEdit, slider):
        value = float(lineEdit.text())
        self.variables[variable] = value  # Edit this
        slider.blockSignals(True)
        slider.setValue(value)
        slider.blockSignals(False)
        self.update()

    def update_from_slider(self, variable, slider, lineEdit):
        value = slider.value()
        self.variables[variable] = value  # Edit this
        lineEdit.blockSignals(True)
        lineEdit.setText('{0}'.format(value))
        lineEdit.setCursorPosition(0)
        lineEdit.blockSignals(False)
        # print('{0} set to {1}'.format(variable, self.variables[variable]))
        self.update()

    def openSliderWindow(self, slider):
        """Open the slider settings window."""
        self.dialog = slider_win(slider)
        self.dialog.show()

    # %% ################# update function #######################
    def update(self):
        """Temporary docstring."""
        # Calculate and plot
        for idx, z in enumerate(self.z_array):
            r = [0, 0, z]
            self.Bz[idx] = field_anti_helmholtz(self.variables['T']
                                                ,self.variables['R']
                                                ,self.variables['D']
                                                ,self.variables['I']
                                                ,r)[2]

        x = self.z_array
        y = self.Bz*10**4
        self.curve_plot1_1.setData(x, y)

        x = self.z_array[:-1]
        y = np.diff(self.Bz*10**4)/np.diff(self.z_array*10**2)
        self.curve_plot2_1.setData(x, y)


if __name__ == '__main__':
    print('main')
    root = QtWidgets.QApplication(sys.argv)
    app = Window()
    sys.exit(root.exec_())
