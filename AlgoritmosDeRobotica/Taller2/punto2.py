# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Botón Graficar
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 40, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(255, 85, 127);")
        self.pushButton.setObjectName("pushButton")

        # ComboBox para seleccionar función
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 40, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook")
        font.setPointSize(12)
        font.setBold(True)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: rgb(170, 0, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("SENO")
        self.comboBox.addItem("COSENO")
        self.comboBox.addItem("TANGENTE")
        self.comboBox.addItem("COTANGENTE")
        self.comboBox.addItem("SECANTE")
        self.comboBox.addItem("COSECANTE")

        # Input para valor mínimo
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(60, 200, 104, 70))
        self.textEdit.setObjectName("textEdit")

        # Label para valor mínimo
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 170, 141, 16))
        self.label.setStyleSheet("color: rgb(170, 0, 127);")
        self.label.setObjectName("label")

        # Input para valor máximo
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(60, 300, 104, 70))
        self.textEdit_2.setObjectName("textEdit_2")

        # Label para valor máximo
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 280, 141, 16))
        self.label_2.setStyleSheet("color: rgb(170, 0, 127);")
        self.label_2.setObjectName("label_2")

        # GraphicsView para mostrar la gráfica
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(290, 180, 256, 192))
        self.graphicsView.setObjectName("graphicsView")

        # Figura para Matplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Conectar el botón a la función para graficar
        self.pushButton.clicked.connect(self.plot_function)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graficador de Funciones"))
        self.pushButton.setText(_translate("MainWindow", "GRAFICAR"))
        self.label.setText(_translate("MainWindow", "INGRESE VALOR MINIMO "))
        self.label_2.setText(_translate("MainWindow", "INGRESE VALOR MAXIMO "))

    def plot_function(self):
        # Obtener valores del comboBox y los textEdits
        func_type = self.comboBox.currentText()
        try:
            min_val = float(self.textEdit.toPlainText())
            max_val = float(self.textEdit_2.toPlainText())
        except ValueError:
            return  # Si los valores no son válidos, no hace nada

        # Crear el rango de valores para x
        x = np.linspace(min_val, max_val, 400)
        y = None

        # Elegir la función a graficar
        if func_type == "SENO":
            y = np.sin(x)
        elif func_type == "COSENO":
            y = np.cos(x)
        elif func_type == "TANGENTE":
            y = np.tan(x)
        elif func_type == "COTANGENTE":
            y = 1 / np.tan(x)
        elif func_type == "SECANTE":
            y = 1 / np.cos(x)
        elif func_type == "COSECANTE":
            y = 1 / np.sin(x)

        if y is not None:
            # Limpiar la figura anterior y graficar la nueva
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            ax.set_title(f"Gráfico de {func_type}")
            self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())