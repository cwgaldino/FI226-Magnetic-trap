#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyQt_utils test window."""

from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from pyQt_utils import slider_win, setSlider, mySlider
import sys


class Window(QtWidgets.QWidget):
    """Temporary docstring."""

    def __init__(self, parent=None):
        super().__init__()

        self.saveBtn = QtGui.QPushButton('set Slider', self)
        self.saveBtn.move(50, 20)
        self.slider1 = mySlider(QtCore.Qt.Horizontal, self)
        setSlider(self.slider1, 0, 10, .3)
        # self.slider1.setMinimum(0)
        # self.slider1.setMaximum(10)
        # self.slider1.setStep(.3)
        self.slider1.valueChanged.connect(self.test)
        self.saveBtn.clicked.connect(self.on_Button_clicked)

        self.show()

    def test(self):
        print(self.slider1.value())

    def on_Button_clicked(self):
        self.dialog = slider_win(self.slider1, parent=self)
        self.dialog.show()


if __name__ == '__main__':
    print('main')
    root = QtWidgets.QApplication(sys.argv)
    app = Window()
    sys.exit(root.exec_())
