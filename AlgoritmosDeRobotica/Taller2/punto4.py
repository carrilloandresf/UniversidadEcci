# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-30, 350, 831, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Slider for voltage
        self.slider_volt = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_volt.setMinimum(1)
        self.slider_volt.setMaximum(20)
        self.slider_volt.setOrientation(QtCore.Qt.Vertical)
        self.slider_volt.setObjectName("slider_volt")
        self.horizontalLayout.addWidget(self.slider_volt)

        # Slider for capacitance
        self.slider_cap = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_cap.setMinimum(1)
        self.slider_cap.setMaximum(100)
        self.slider_cap.setOrientation(QtCore.Qt.Vertical)
        self.slider_cap.setObjectName("slider_cap")
        self.horizontalLayout.addWidget(self.slider_cap)

        # Slider for resistance
        self.slider_res = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_res.setMinimum(1)
        self.slider_res.setMaximum(1000)
        self.slider_res.setOrientation(QtCore.Qt.Vertical)
        self.slider_res.setObjectName("slider_res")
        self.horizontalLayout.addWidget(self.slider_res)

        # Label layout
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 290, 661, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_volt = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_volt.setFont(font)
        self.label_volt.setMouseTracking(False)
        self.label_volt.setStyleSheet("background-color: rgb(255, 85, 255);")
        self.label_volt.setWordWrap(True)
        self.label_volt.setObjectName("label_volt")
        self.horizontalLayout_2.addWidget(self.label_volt)

        self.label_cap = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_cap.setFont(font)
        self.label_cap.setStyleSheet("background-color: rgb(255, 85, 127);")
        self.label_cap.setWordWrap(True)
        self.label_cap.setObjectName("label_cap")
        self.horizontalLayout_2.addWidget(self.label_cap)

        self.label_res = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(16)
        font.setBold(True)
        self.label_res.setFont(font)
        self.label_res.setStyleSheet("background-color: rgb(170, 85, 127);")
        self.label_res.setWordWrap(True)
        self.label_res.setObjectName("label_res")
        self.horizontalLayout_2.addWidget(self.label_res)

        # Widget for matplotlib figure
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(220, 30, 341, 221))
        self.widget.setObjectName("widget")

        # Layout for graph
        self.graph_layout = QVBoxLayout(self.widget)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.graph_layout.addWidget(self.canvas)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect sliders to the function that updates the graph
        self.slider_volt.valueChanged.connect(self.update_graph)
        self.slider_cap.valueChanged.connect(self.update_graph)
        self.slider_res.valueChanged.connect(self.update_graph)

        self.update_graph()  # Initial call to draw the graph with default values

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_volt.setText(_translate("MainWindow", "VOLTAJE (V)"))
        self.label_cap.setText(_translate("MainWindow", "CAPACITANCIA (uF)"))
        self.label_res.setText(_translate("MainWindow", "RESISTENCIA (ohms)"))

    def update_graph(self):
        # Get values from sliders
        V = self.slider_volt.value()  # Voltaje
        C = self.slider_cap.value() * 1e-6  # Capacitancia in Farads
        R = self.slider_res.value()  # Resistencia

        # Time for plotting
        t = np.linspace(0, 5, 500)
        
        # Calculate the charge/discharge voltage of the capacitor (RC circuit)
        tau = R * C
        Vc = V * (1 - np.exp(-t / tau))  # Charging equation

        # Clear previous plot
        self.ax.clear()
        
        # Plot the capacitor charging curve
        self.ax.plot(t, Vc, label="Carga del condensador")
        self.ax.set_title('Carga del Condensador')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Voltaje (V)')
        self.ax.legend()
        self.ax.grid(True)

        # Refresh the canvas
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
