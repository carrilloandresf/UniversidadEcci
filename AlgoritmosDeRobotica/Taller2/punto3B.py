# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO
import time

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

        # Label para la descripción del lineEdit
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(250, 120, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        # Label del título
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(330, 10, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Campo de texto para ingresar el tiempo
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(350, 70, 151, 41))
        self.lineEdit.setObjectName("lineEdit")

        # Botón para iniciar el conteo regresivo
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 170, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        # Label para mostrar el conteo regresivo
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(350, 220, 151, 41))
        self.label_5.setObjectName("label_5")

        # Label para mostrar la lectura del sensor
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(360, 280, 111, 31))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conectar el evento del botón
        self.pushButton.clicked.connect(self.start_countdown)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Control de Sensor"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Daniela Rodriguez 83549</p><p align=\"center\">Jeison Sanchez 61849</p><p align=\"center\">Andres C. Rodriguez 83836</p><p align=\"center\">William A. Fernandez 77516</p><p><br/></p><p><br/></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "INGRESE TIEMPO ESTIMADO EN SEGUNDOS"))
        self.label.setText(_translate("Dialog", "Comunicación I2C"))
        self.pushButton.setText(_translate("Dialog", "INICIAR"))
        self.label_5.setText(_translate("Dialog", "MUESTRA LA LECTURA"))
        self.label_6.setText(_translate("Dialog", "LECTURA DEL SENSOR"))

    def start_countdown(self):
        try:
            # Obtener el valor del tiempo ingresado por el usuario
            countdown_time = int(self.lineEdit.text())
        except ValueError:
            self.label_5.setText("Por favor, ingrese un número válido")
            return

        # Iniciar el conteo regresivo
        for remaining_time in range(countdown_time, -1, -1):
            # Mostrar el tiempo restante en `label_5`
            self.label_5.setText(f"Tiempo restante: {remaining_time}s")

            # Leer el valor del sensor
            sensor_value = GPIO.input(SENSOR_PIN)

            # Mostrar el valor del sensor en `label_6`
            self.label_6.setText(f"Lectura: {sensor_value}")

            # Esperar un segundo antes de la siguiente iteración
            QtCore.QCoreApplication.processEvents()  # Procesar eventos de la interfaz
            time.sleep(1)

    def closeEvent(self, event):
        # Limpiar los recursos de GPIO al cerrar
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
