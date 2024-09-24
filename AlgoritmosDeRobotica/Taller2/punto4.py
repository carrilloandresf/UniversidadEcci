# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
import matplotlib
matplotlib.use('Qt5Agg')  # Utilizar el backend para PyQt5
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 715)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout de sliders
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-30, 350, 831, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Slider para el voltaje
        self.slider_volt = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_volt.setMinimum(1)
        self.slider_volt.setMaximum(20)
        self.slider_volt.setOrientation(QtCore.Qt.Vertical)
        self.slider_volt.setObjectName("slider_volt")
        self.horizontalLayout.addWidget(self.slider_volt)

        # Slider para la capacitancia
        self.slider_cap = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_cap.setMinimum(1)
        self.slider_cap.setMaximum(100)
        self.slider_cap.setOrientation(QtCore.Qt.Vertical)
        self.slider_cap.setObjectName("slider_cap")
        self.horizontalLayout.addWidget(self.slider_cap)

        # Slider para la resistencia
        self.slider_res = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.slider_res.setMinimum(1)
        self.slider_res.setMaximum(1000)
        self.slider_res.setOrientation(QtCore.Qt.Vertical)
        self.slider_res.setObjectName("slider_res")
        self.horizontalLayout.addWidget(self.slider_res)

        # Labels para mostrar valores de sliders
        self.label_val_volt = QtWidgets.QLabel(self.centralwidget)
        self.label_val_volt.setGeometry(QtCore.QRect(60, 520, 120, 20))
        self.label_val_volt.setObjectName("label_val_volt")

        self.label_val_cap = QtWidgets.QLabel(self.centralwidget)
        self.label_val_cap.setGeometry(QtCore.QRect(240, 520, 120, 20))
        self.label_val_cap.setObjectName("label_val_cap")

        self.label_val_res = QtWidgets.QLabel(self.centralwidget)
        self.label_val_res.setGeometry(QtCore.QRect(420, 520, 120, 20))
        self.label_val_res.setObjectName("label_val_res")

        # Label para la fórmula utilizada
        self.label_formula = QtWidgets.QLabel(self.centralwidget)
        self.label_formula.setGeometry(QtCore.QRect(60, 560, 600, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_formula.setFont(font)
        self.label_formula.setObjectName("label_formula")

        # Sección para el logo
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(60, 490, 131, 41))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("logo.png"))  # Asegúrate de poner la ruta correcta del logo
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")

        # Sección para los nombres del equipo
        self.label_equipo = QtWidgets.QLabel(self.centralwidget)
        self.label_equipo.setGeometry(QtCore.QRect(60, 390, 221, 81))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_equipo.setFont(font)
        self.label_equipo.setObjectName("label_equipo")

        # Widget para el gráfico de matplotlib
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(220, 30, 341, 221))
        self.widget.setObjectName("widget")

        # Layout para el gráfico
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

        # Conectar los sliders a la función que actualiza el gráfico y los valores de los labels
        self.slider_volt.valueChanged.connect(self.update_graph)
        self.slider_cap.valueChanged.connect(self.update_graph)
        self.slider_res.valueChanged.connect(self.update_graph)

        self.update_graph()  # Llamada inicial para dibujar el gráfico con valores predeterminados

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulador RC Circuito"))
        self.label_val_volt.setText(_translate("MainWindow", "Voltaje (V): 1"))
        self.label_val_cap.setText(_translate("MainWindow", "Capacitancia (uF): 1"))
        self.label_val_res.setText(_translate("MainWindow", "Resistencia (Ohms): 1"))
        self.label_formula.setText(_translate("MainWindow", "Fórmula: Vc = V * (1 - exp(-t / (R*C)))"))
        self.label_equipo.setText(_translate("MainWindow", "<html><body><p>Andrés Felipe Carrillo Rodríguez<br>Daniela Rodríguez Pelaez<br>Jeisson Gutierrez Sanchez<br>William Alejandro Fernandez Pinzón</p><p>Ingeniería Mecatrónica<br>Electiva de Robótica<br>2024 - II</p></body></html>"))

    def update_graph(self):
        # Obtener valores de los sliders
        V = self.slider_volt.value()  # Voltaje
        C = self.slider_cap.value() * 1e-6  # Capacitancia en Farads
        R = self.slider_res.value()  # Resistencia

        # Actualizar los labels con los valores actuales
        self.label_val_volt.setText(f"Voltaje (V): {V}")
        self.label_val_cap.setText(f"Capacitancia (uF): {self.slider_cap.value()}")
        self.label_val_res.setText(f"Resistencia (Ohms): {R}")

        # Tiempo para la graficación
        t = np.linspace(0, 5, 500)
        
        # Calcular la carga/descarga del condensador (ecuación RC)
        tau = R * C
        Vc = V * (1 - np.exp(-t / tau))  # Ecuación de carga

        # Limpiar el gráfico anterior
        self.ax.clear()
        
        # Graficar la curva de carga del condensador
        self.ax.plot(t, Vc, label="Carga del condensador")
        self.ax.set_title('Carga del Condensador')
        self.ax.set_xlabel('Tiempo (s)')
        self.ax.set_ylabel('Voltaje (V)')
        self.ax.legend()
        self.ax.grid(True)

        # Refrescar el canvas del gráfico
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
