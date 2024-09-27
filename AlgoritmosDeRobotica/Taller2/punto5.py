# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import smbus  # Para comunicación I2C con el MPU-6050
import time

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(860, 640)
        
        # Botón para iniciar la lectura
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(340, 340, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        # Label para mostrar la lectura del sensor
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(320, 110, 231, 201))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Campo de texto para ingresar el tiempo de visualización
        self.timeEdit = QtWidgets.QLineEdit(Dialog)
        self.timeEdit.setGeometry(QtCore.QRect(320, 280, 231, 40))
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setPlaceholderText("Tiempo de visualización (s)")

        # Conectar el botón con la función para leer el sensor
        self.pushButton.clicked.connect(self.read_sensor)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Configurar el bus I2C y el MPU-6050
        self.bus = smbus.SMBus(1)  # Usar I2C bus 1
        self.device_address = 0x68  # Dirección I2C del MPU-6050
        self.bus.write_byte_data(self.device_address, 0x6B, 0)  # Despertar al MPU-6050

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lectura de Sensor MPU-6050"))
        self.pushButton.setText(_translate("Dialog", "Leer Sensor"))

    def read_sensor(self):
        # Obtener el tiempo de visualización ingresado por el usuario
        try:
            display_time = int(self.timeEdit.text())
        except ValueError:
            display_time = 5  # Valor por defecto si no es un número válido

        # Leer datos de aceleración del MPU-6050
        acc_x = self.read_raw_data(0x3B)
        acc_y = self.read_raw_data(0x3D)
        acc_z = self.read_raw_data(0x3F)
        
        # Calcular las lecturas de aceleración reales
        ax = acc_x / 16384.0
        ay = acc_y / 16384.0
        az = acc_z / 16384.0

        # Mostrar los datos en el label
        self.label.setText(f"Aceleración X: {ax:.2f}g\nAceleración Y: {ay:.2f}g\nAceleración Z: {az:.2f}g")

        # Mostrar la lectura durante el tiempo especificado
        QtCore.QTimer.singleShot(display_time * 1000, self.clear_label)

    def clear_label(self):
        # Limpiar el label después del tiempo especificado
        self.label.setText("")

    def read_raw_data(self, addr):
        # Leer datos crudos de 16 bits del sensor
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)
        value = ((high << 8) | low)
        # Convertir a complemento a dos
        if value > 32768:
            value = value - 65536
        return value

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
