"""
@file   euler.py
@author elijw
@date   2026-03-13
@brief  Big ugly monolith at the moment but it works (well enough, that is...)
        This code is atrocious.
"""

import sys
import random

import matplotlib.pyplot as plt
import numpy as numpy
import sympy as sp

from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #### GUI COMPONENTS ####

        # text input stuff
        self.eqn_label = QtWidgets.QLabel("f(x,y)")
        self.eqn_input = QtWidgets.QLineEdit()

        # x_0 stuff
        self.x0_label = QtWidgets.QLabel("x_0")
        self.x0_spin = QtWidgets.QSpinBox(value=-0, minimum=-200, maximum=200)

        # y_0 stuff
        self.y0_label = QtWidgets.QLabel("y_0")
        self.y0_spin = QtWidgets.QSpinBox(value=0, minimum=-200, maximum=200)

        # step size stuff
        self.h0_label = QtWidgets.QLabel("h_0")
        self.h0_spin = QtWidgets.QDoubleSpinBox(value=0.1, minimum=0.0001, maximum=2.0, singleStep=0.1)
        
        self.h1_label = QtWidgets.QLabel("h_1")
        self.h1_spin = QtWidgets.QDoubleSpinBox(value=0.01, minimum=0.0001, maximum=2.0, singleStep=0.01)
      

        #### VALUES ####

        # equation stuff
        self.eqn = None 
        self.eqn_input.textChanged.connect(self.get_f)

        # init values
        self.x0 = float(self.x0_spin.value())
        self.y0 = float(self.y0_spin.value())
        self.h1 = float(self.h0_spin.value())
        self.h2 = float(self.h1_spin.value())
        self.s1 = int(self.s1_spin.value())
        self.s2 = int((self.h1 * self.s1) / self.h2)
        
        # init x and y value lists
        self.x1 = [self.x0]
        self.y1 = [self.y0]
        self.x2 = [self.x0]
        self.y2 = [self.y0]

        # step count stuff
        self.s1_label = QtWidgets.QLabel("s1")
        self.s1_spin = QtWidgets.QSpinBox(value=20, minimum=1, maximum=100)
        self.s2_label = QtWidgets.QLabel("s2")
        self.s2_spin = QtWidgets.QLabel(str(int((self.h1 * self.s1) / self.h2)))

        # graph button
        self.graph_button = QtWidgets.QPushButton("Graph")


        #### LAYOUT ####
        
        # main layout
        self.l_main = QtWidgets.QGridLayout(self)
 
        # sub-layout for equation input
        self.l_eqn = QtWidgets.QHBoxLayout()
        self.l_eqn.addWidget(self.eqn_label)
        self.l_eqn.addWidget(self.eqn_input)
        # add equation layout to main layout
        self.l_main.addLayout(self.l_eqn, 0, 0)

        # sub-layout for initial values
        self.l_iv = QtWidgets.QHBoxLayout()
        # # sub-sub-layout for x_0 stuff
        self.l_x0 = QtWidgets.QHBoxLayout()
        self.l_x0.addWidget(self.x0_label)
        self.l_x0.addWidget(self.x0_spin)
        self.l_iv.addLayout(self.l_x0)
        # # sub-sub-layout for y_0 stuff
        self.l_y0 = QtWidgets.QHBoxLayout()
        self.l_y0.addWidget(self.y0_label)
        self.l_y0.addWidget(self.y0_spin)
        self.l_iv.addLayout(self.l_y0)
        # add iv layout to main
        self.l_main.addLayout(self.l_iv, 1, 0)

        # sub-layout for step size inputs
        self.l_h = QtWidgets.QHBoxLayout()
        # # sub-sub-layout for first graph step size
        self.l_h0 = QtWidgets.QHBoxLayout()
        self.l_h0.addWidget(self.h0_label)
        self.l_h0.addWidget(self.h0_spin)
        self.l_h.addLayout(self.l_h0)
        # # sub-sub-layout for first graph step size
        self.l_h1 = QtWidf.l_h1.addWidget(self.h1_label)
        self.l_h1.addWidget(self.h1_spin)
        self.l_h.addLayout(self.l_h1)
        # add step size sub-layout to main layout
        self.l_main.addLayout(self.l_h, 2 ,0)

        # sub-layout for step count stuff 
        self.l_s = QtWidgets.QHBoxLayout()
        # # sub-sub-layout for step size 1
        self.l_s1 = QtWidgets.QHBoxLayout()
        self.l_s1.addWidget(self.s1_label)
        self.l_s1.addWidget(self.s1_spin)
        self.l_s.addLayout(self.l_s1)
        # # sub-sub-layout for step size 2
        self.l_s2 = QtWidgets.QHBoxLayout()
        self.l_s2.addWidget(self.s2_label)
        self.l_s2.addWidget(self.s2_spin)
        self.l_s.addLayout(self.l_s2)
        # add step count sub-layout to main layout
        self.l_main.addLayout(self.l_s, 3, 0)

        # add "graph" button to layout
        self.l_main.addWidget(self.graph_button, 4, 0, alignment=QtCore.Qt.AlignCenter)

        # actions
        self.graph_button.clicked.connect(self.graph)


    """
    here we take the value from the QLineEdit field and use sympy
    to evaluate the user provided f(x,y) and turn it into a func
    """
    @QtCore.Slot()
    def get_f(self):
        expr_str = str(self.eqn_input.text())
        
        # logging excellence
        print(f"[DEBUG]: {self.eqn_input.text()}")
        
        x, y = sp.symbols('x y')
        expr = sp.sympify(expr_str)

        self.eqn = sp.lambdify((x, y), expr, "numpy")


    """
    the meat and potatoes.
    """
    @QtCore.Slot()
    def process(self, f, h, s, x_vals, y_vals):
        for i in range(s):
            x_n = x_vals[-1]
            y_n = y_vals[-1]

            y_next = y_n + h * f(x_n, y_n)
            x_next = x_n + h

            x_vals.append(x_next)
            y_vals.append(y_next)

        print(f"Step size {h}, {s} steps.")
        for j in range(len(x_vals)):
            print(f"{j}\t{x_vals[j]:.4f}\t{y_vals[j]:.4f}")
        print()

        return x_vals, y_vals


    """
    
    """
    @QtCore.Slot()
    def graph(self):
        self.get_f()

        # get values from widgets
        self.x0 = float(self.x0_spin.value())
        self.y0 = float(self.y0_spin.value())
        self.h1 = float(self.h0_spin.value())
        self.h2 = float(self.h1_spin.value())
        self.s1 = int(self.s1_spin.value())
        self.s2 = int((self.h1 * self.s1) / self.h2)

        self.s2_spin.setText(str(self.s2))

        self.x1 = [self.x0]
        self.y1 = [self.y0]
        self.x2 = [self.x0]
        self.y2 = [self.y0]
 
        self.x1, self.y1 = self.process(self.eqn, self.h1, self.s1, self.x1, self.y1)
        self.x2, self.y2 = self.process(self.eqn, self.h2, self.s2, self.x2, self.y2)
        
        fig, axs = plt.subplots(2, sharex=True)
   
        axs[0].plot(self.x1, self.y1, marker="o")
        axs[0].set_title(f"h = {self.h1}")
        axs[0].set_ylabel("y")
        axs[0].grid(True)

        axs[1].plot(self.x2, self.y2, marker="o")
        axs[1].set_title(f"h = {self.h2}")
        axs[1].set_xlabel("x")
        axs[1].set_ylabel("y")
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    #widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
