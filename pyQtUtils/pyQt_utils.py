#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilities for building pyQt applications (GUI's).

Todo
----
Document all functions.
"""

# from pyqtgraph.Qt import QtCore
# from PyQt5.QtWidgets import QSlider
from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import uic, QtWidgets


class slider_win(QtGui.QWidget):
    """Opens a dedicated window to edit the parameters of a slider.

    More than often, I like to edit the parameters of a slider when the app is
    already running. This opens a dedicated window from within the app that
    allows you to change the slider parameters.

    Args:
        slider (QtWidgets.QSlider): The slider instance.
    """

    def __init__(self, slider, parent=None):
        """Init method.

        Args:
            slider (QtWidgets.QSlider): The slider instance.
        """
        super().__init__()
        uic.loadUi('slider.ui', self)
        self.slider = slider

        self.set_text()  # data on text boxes

        self.btn1.clicked.connect(self.update)
        self.btn2.clicked.connect(self.close_win)

    def update(self):
        self.slider.setMinimum(float(self.lineEdit.text()))
        self.slider.setMaximum(float(self.lineEdit_1.text()))
        self.slider.setStep(float(self.lineEdit_2.text()))
        self.set_text()
        self.close()

    def set_text(self):
        self.lineEdit.setText('{0}'.format(self.slider.minimum()))
        self.lineEdit_1.setText('{0}'.format(self.slider.maximum()))
        self.lineEdit_2.setText(str(self.slider.getStep()))

    def close_win(self):
        self.close()


def setSlider(slider, min, max, step):
    """Set slider parameters with one line of code."""
    slider.setMinimum(min)
    slider.setMaximum(max)
    slider.setStep(step)


class mySlider(QtWidgets.QSlider):
    """Same as QtWidgets.QSlider, but with float steps."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step = 1

    def setStep(self, newStep):
        max = self.maximum()
        min = self.minimum()
        value = self.value()
        self.step = newStep
        self.setMaximum(max)
        self.setMinimum(min)
        self.setValue(value)

    def getStep(self):
        return self.step

    def setMinimum(self, min):
        super().setMinimum(int(min/self.step))

    def setMaximum(self, max):
        super().setMaximum(int(max/self.step))

    def minimum(self):
        return super().minimum()*self.step

    def maximum(self):
        return super().maximum()*self.step

    def value(self):
        return super().value()*self.step

    def setValue(self, value):
        return super().setValue(int(value/self.step))
