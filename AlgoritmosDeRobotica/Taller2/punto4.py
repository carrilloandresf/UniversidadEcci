# -*- coding: utf-8 -*-

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Título y logo de la universidad
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(600, 20, 100, 100))
        self.label_logo.setPixmap(QtGui.QPixmap("logoUniversidadEcci.jpg"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")

        self.label_equipo = QtWidgets.QLabel(self.centralwidget)
        self.label_equipo.setGeometry(QtCore.QRect(50, 20, 500, 80))
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.label_equipo.setFont(font)
        self.label_equipo.setAlignment(QtCore.Qt.AlignLeft)
        self.label_equipo.setObjectName("label_equipo")

        # Gráfica usando QGraphicsView
        self.Grafica = QtWidgets.QGraphicsView(self.centralwidget)
        self.Grafica.setGeometry(QtCore.QRect(100, 120, 600, 250))
        self.Grafica.setObjectName("Grafica")
        self.scene = QGraphicsScene()
        self.Grafica.setScene(self.scene)

        # Sliders para resistencia, voltaje y capacitancia
        self.label_res = QtWidgets.QLabel(self.centralwidget)
        self.label_res.setGeometry(QtCore.QRect(100, 400, 200, 20))
        self.label_res.setAlignment(QtCore.Qt.AlignCenter)
        self.label_res.setText("Resistencia (Ohms):")
        self.label_res.setObjectName("label_res")

        self.Resistencia = QtWidgets.QSlider(self.centralwidget)
        self.Resistencia.setGeometry(QtCore.QRect(100, 420, 200, 20))
        self.Resistencia.setMinimum(1)
        self.Resistencia.setMaximum(1000)
        self.Resistencia.setOrientation(QtCore.Qt.Horizontal)
        self.Resistencia.setObjectName("Resistencia")

        self.label_vol = QtWidgets.QLabel(self.centralwidget)
        self.label_vol.setGeometry(QtCore.QRect(300, 400, 200, 20))
        self.label_vol.setAlignment(QtCore.Qt.AlignCenter)
        self.label_vol.setText("Voltaje (V):")
        self.label_vol.setObjectName("label_vol")

        self.Voltaje = QtWidgets.QSlider(self.centralwidget)
        self.Voltaje.setGeometry(QtCore.QRect(300, 420, 200, 20))
        self.Voltaje.setMinimum(1)
        self.Voltaje.setMaximum(20)
        self.Voltaje.setOrientation(QtCore.Qt.Horizontal)
        self.Voltaje.setObjectName("Voltaje")

        self.label_cap = QtWidgets.QLabel(self.centralwidget)
        self.label_cap.setGeometry(QtCore.QRect(500, 400, 200, 20))
        self.label_cap.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cap.setText("Capacitancia (uF):")
        self.label_cap.setObjectName("label_cap")

        self.Capacitancia = QtWidgets.QSlider(self.centralwidget)
        self.Capacitancia.setGeometry(QtCore.QRect(500, 420, 200, 20))
        self.Capacitancia.setMinimum(1)
        self.Capacitancia.setMaximum(1000)  # Ajustar el máximo a 1000 uF
        self.Capacitancia.setOrientation(QtCore.Qt.Horizontal)
        self.Capacitancia.setObjectName("Capacitancia")

        # Labels para mostrar los valores actuales de los sliders
        self.label_val_res = QtWidgets.QLabel(self.centralwidget)
        self.label_val_res.setGeometry(QtCore.QRect(100, 450, 200, 20))
        self.label_val_res.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_res.setObjectName("label_val_res")

        self.label_val_volt = QtWidgets.QLabel(self.centralwidget)
        self.label_val_volt.setGeometry(QtCore.QRect(300, 450, 200, 20))
        self.label_val_volt.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_volt.setObjectName("label_val_volt")

        self.label_val_cap = QtWidgets.QLabel(self.centralwidget)
        self.label_val_cap.setGeometry(QtCore.QRect(500, 450, 200, 20))
        self.label_val_cap.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val_cap.setObjectName("label_val_cap")

        # Label para la fórmula
        self.label_formula = QtWidgets.QLabel(self.centralwidget)
        self.label_formula.setGeometry(QtCore.QRect(100, 480, 600, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_formula.setFont(font)
        self.label_formula.setAlignment(QtCore.Qt.AlignCenter)
        self.label_formula.setObjectName("label_formula")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Conectar sliders con la función de actualización de la gráfica
        self.Resistencia.valueChanged.connect(self.datos)
        self.Capacitancia.valueChanged.connect(self.datos)
        self.Voltaje.valueChanged.connect(self.datos)

        self.configurar()  # Llamada inicial para configurar la gráfica

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulador RC Circuito"))
        self.label_val_volt.setText(_translate("MainWindow", "Voltaje (V): 1"))
        self.label_val_cap.setText(_translate("MainWindow", "Capacitancia (uF): 1"))
        self.label_val_res.setText(_translate("MainWindow", "Resistencia (Ohms): 1"))
        self.label_formula.setText(_translate("MainWindow", "Fórmula (Carga y Descarga): Vc = V * (1 - exp(-t / (R*C))) para carga, Vc = V * exp(-t / (R*C)) para descarga"))
        self.label_equipo.setText(_translate("MainWindow", "<html><body><p>Andrés Felipe Carrillo Rodríguez<br>Daniela Rodríguez Pelaez<br>Jeisson Gutierrez Sanchez<br>William Alejandro Fernandez Pinzón</p><p>Ingeniería Mecatrónica<br>Electiva de Robótica<br>2024 - II</p></body></html>"))

    def configurar(self):
        # Configurar la figura para la gráfica
        self.figure = Figure(figsize=(3, 2))
        self.canvas = FigureCanvas(self.figure)
        self.scene.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.datos()

    def datos(self):
        # Obtener valores de sliders
        R = self.Resistencia.value()
        C = self.Capacitancia.value() * 1e-6  # Convertir de uF a Faradios
        V = self.Voltaje.value()

        # Actualizar los labels con los valores actuales
        self.label_val_volt.setText(f"Voltaje (V): {V}")
        self.label_val_cap.setText(f"Capacitancia (uF): {self.Capacitancia.value()}")  # Mostrar uF en lugar de Faradios
        self.label_val_res.setText(f"Resistencia (Ohms): {R}")

        # Tiempo para la graficación
        t = np.linspace(0, 1, 4000)

        # Calcular la carga y descarga del condensador
        Carga = self.carga(V, R, C, t)
        Descarga = self.descarga(V, R, C, t)

        # Limpiar el gráfico anterior
        self.ax.clear()

        # Graficar la carga y descarga del condensador
        self.ax.plot(t, Carga, label="Carga")
        self.ax.plot(t, Descarga, label="Descarga", linestyle="--")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.ax.legend()

        # Refrescar el canvas del gráfico
        self.canvas.draw()

    def carga(self, V, R, C, t):
        return V * (1 - np.exp(-t / (R * C)))

    def descarga(self, V, R, C, t):
        return V * np.exp(-t / (R * C))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
