# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO

# Configuración del pin GPIO para la lectura del sensor
SENSOR_PIN = 4

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(860, 640)

        # Label principal
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 440, 261, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        # Logo de la universidad
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(450, 400, 271, 161))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("logoUniversidadEcci.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")

        # Label del título
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(260, 50, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Label para mostrar el estado del pin
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(330, 110, 201, 91))
        self.label_5.setObjectName("label_5")

        # Label para mostrar la lectura del sensor
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(350, 200, 241, 31))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Configurar un temporizador para leer el sensor periódicamente
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_sensor_reading)
        self.timer.start(1000)  # Leer el sensor cada 1000 ms (1 segundo)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Control de Sensor"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Daniela Rodriguez 83549</p><p align=\"center\">Jeison Sanchez   61849</p><p align=\"center\">Andres C. Rodriguez  83836</p><p align=\"center\">William A. Fernandez 77516</p><p><br/></p><p><br/></p></body></html>"))
        self.label.setText(_translate("Dialog", "Lectura de puertos digitales"))
        self.label_5.setText(_translate("Dialog", "MUESTRA EL ESTADO DEL PIN"))
        self.label_6.setText(_translate("Dialog", "ESTADO DEL PIN"))

    def update_sensor_reading(self):
        # Leer el valor del sensor
        sensor_value = GPIO.input(SENSOR_PIN)
        print_sensor = "Bajo"

        if sensor_value == 1:
            print_sensor = "Bajo"
            self.label_6.setStyleSheet("background-color: green;")

        elif sensor_value == 0:
            print_sensor = "Alto"
            self.label_6.setStyleSheet("background-color: red;")    

        # Actualizar `label_6` con el valor del sensor
        self.label_6.setText(f"Lectura: {print_sensor}")

    def closeEvent(self, event):
        # Detener el temporizador y limpiar los recursos de GPIO al cerrar
        self.timer.stop()
        GPIO.cleanup()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())