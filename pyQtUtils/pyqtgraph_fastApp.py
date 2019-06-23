#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template to build pyqt application using pyqtgraph's dock widget system.

-Use the slider lineEdit for values that are sometimes not reachble within the
resolution of the slider.

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
# from pathlib import Path
# import copy

from pyQt_utils import slider_win, setSlider, mySlider

class Window(QtGui.QMainWindow):
    """Temp docstring."""

    def __init__(self):
        """Temp docstring."""
        super().__init__()

        # %% ########### variables parameters ########################
        # parameter table 1
        self.variables      = dict(x=5, y=2, z=2)
        self.variables_min  = dict(x=0, y=0, z=0)
        self.variables_max  = dict(x=10,y=10,z=10)
        self.variables_step = dict(x=1, y=.1,z=.3)
        self.variables_txt = dict(x='(m)',   y='(cm)',  z='(some comment)')
        self.table1 = list(self.variables.keys())

        # parameter table 2
        self.variables.update(dict(x2=0, y2=11.8))
        self.variables_min.update(dict(x2=-10, y2=-5))
        self.variables_max.update(dict(x2=10, y2=20))
        self.variables_step.update(dict(x2=1, y2=.2))
        self.variables_txt.update(dict(x2=None,   y=None,  z=None))
        self.table2 = [x for x in list(self.variables.keys()) if x not in self.table1]

        # parameter table 3
        self.variables.update(dict(x3=2))
        self.variables_min.update(dict(x3=0))
        self.variables_max.update(dict(x3=3))
        self.variables_step.update(dict(x3=1))
        self.variables_txt.update(dict(x3=None))
        self.table3 = [x for x in list(self.variables.keys()) if x not in self.table1 and x not in self.table2]

        # %% ########## window parameters ############
        self.resize(1000, 800)
        self.setWindowTitle('pyqtgraph_fastApp')

        # %% ########## Init dockable area ###############
        self.area = DockArea()
        self.setCentralWidget(self.area)

        # %% ################ Create and place docks ##################
        self.d1 = Dock("plot 1 (d1)", size=(1, 1), closable=True)
        self.d2 = Dock("plot 2 (d2)", size=(1, 1), closable=True)
        self.d3 = Dock("parameter table 1 (d3)", size=(1, 1))
        self.d4 = Dock("parameter table 2 (d4)", size=(1, 1))
        self.d5 = Dock("parameter table 3 (d5)", size=(1, 1))
        self.d6 = Dock("plot 3 (d6)", size=(1, 1), closable=True)

        self.area.addDock(self.d6, 'left')
        self.area.addDock(self.d1, 'above', self.d6)
        self.area.addDock(self.d2, 'right')

        self.area.addDock(self.d5, 'bottom')
        self.area.addDock(self.d4, 'above', self.d5)
        self.area.addDock(self.d3, 'above', self.d4)

        # Move docks programatically after they have been placed
        # self.area.moveDock(self.d4, 'top', self.d2)  # move d4 to top edge of d2

        # %% #################### dock 1 ########################
        self.w1 = pg.LayoutWidget()
        # self.d1.hideTitleBar()
        # Add (and set) a plot into this dock
        self.w1 = pg.PlotWidget(title=None)
        self.w1.setLabel('bottom', text='x axis', unitPrefix=None)
        self.w1.setLabel('left', text='y axis', unitPrefix=None)
        self.curve_plot1_1 = self.w1.plot([], pen='g')
        self.curve_plot1_2 = self.w1.plot([], pen='r')
        self.d1.addWidget(self.w1)

        # %% #################### dock 2 ########################
        self.w2 = pg.LayoutWidget()
        # self.d1.hideTitleBar()
        # Add (and set) a plot into this dock
        self.w2 = pg.PlotWidget(title=None)
        self.w2.setLabel('bottom', text='x axis', unitPrefix=None)
        self.w2.setLabel('left', text='y axis', unitPrefix=None)
        self.curve_plot2_1 = self.w2.plot([], symbolBrush=None, pen='y')
        self.curve_plot2_2 = self.w2.plot([], pen='g')
        self.d2.addWidget(self.w2)

        # %% #################### dock 6 ########################
        self.w6 = pg.LayoutWidget()
        # self.d1.hideTitleBar()
        # Add (and set) a plot into this dock
        self.w6 = pg.PlotWidget(title=None)
        self.w6.setLabel('bottom', text='x axis', unitPrefix=None)
        self.w6.setLabel('left', text='y axis (cm)', unitPrefix=None)
        self.curve_plot3_1 = self.w6.plot([], symbolBrush=None, pen='r')
        self.curve_plot3_2 = self.w6.plot([])
        self.curve_plot3_3 = self.w6.plot([], pen='g')
        self.d6.addWidget(self.w6)

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

        # %% #################### dock 4 ########################
        # This is a parameter dock.
        self.sliders = dict()
        for idx, variable in enumerate(self.table2):
            value = self.variables[variable]
            min   = self.variables_min[variable]
            max   = self.variables_max[variable]
            step  = self.variables_step[variable]
            txt   = self.variables_txt[variable]
            self.sliders[variable] = self.createSlider(variable, min, max, step, value, txt)

            self.d4.addWidget(self.sliders[variable]['btn'],    row=idx, col=1)
            self.d4.addWidget(self.sliders[variable]['slider'], row=idx, col=2)
            self.d4.addWidget(self.sliders[variable]['txt'],    row=idx, col=3)
            self.d4.addWidget(self.sliders[variable]['lineEdit'], row=idx, col=4)

        # %% #################### dock 5 ########################
        # This is a parameter dock.
        self.sliders = dict()
        for idx, variable in enumerate(self.table3):
            value = self.variables[variable]
            min   = self.variables_min[variable]
            max   = self.variables_max[variable]
            step  = self.variables_step[variable]
            txt   = self.variables_txt[variable]
            self.sliders[variable] = self.createSlider(variable, min, max, step, value, txt)

            self.d5.addWidget(self.sliders[variable]['btn'],    row=idx, col=1)
            self.d5.addWidget(self.sliders[variable]['slider'], row=idx, col=2)
            self.d5.addWidget(self.sliders[variable]['txt'],    row=idx, col=3)
            self.d5.addWidget(self.sliders[variable]['lineEdit'], row=idx, col=4)

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
        x1 = self.variables['x']
        y1 = self.variables['y']
        # z1 = self.variables['z']
        # x2 = self.variables['x2']
        # y2 = self.variables['y2']
        # x3 = self.variables['x3']

        x = np.linspace(0, 10*np.pi, 250)
        y = x1*np.sin(y1*x)
        self.curve_plot1_1.setData(x, y)
        # self.w2.setLimits(xMin=self.variables['min_r'], xMax=self.variables['max_r'])


if __name__ == '__main__':
    print('main')
    root = QtWidgets.QApplication(sys.argv)
    app = Window()
    sys.exit(root.exec_())
