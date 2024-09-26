# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO
import time

# Pines GPIO para el motor paso a paso
MOTOR_PINS = [12, 20, 21, 19]

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
for pin in MOTOR_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Secuencia para el motor paso a paso (ULN2003AN)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Número de pasos por vuelta para el motor
STEPS_PER_REVOLUTION = 4096 / 8  # Ajusta según el motor paso a paso

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
        self.label.setGeometry(QtCore.QRect(290, 40, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Campo de texto para ingresar el número de vueltas
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(350, 110, 151, 41))
        self.lineEdit.setObjectName("lineEdit")

        # Label para describir la entrada de vueltas
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(284, 160, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        # Botón para iniciar el giro del motor
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 220, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conectar el botón al evento de iniciar el motor
        self.pushButton.clicked.connect(self.start_motor)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Control de Motor Paso a Paso"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Daniela Rodriguez 83549</p><p align=\"center\">Jeison Sanchez   61849</p><p align=\"center\">Andres C. Rodriguez  83836</p><p align=\"center\">William A. Fernandez 77516</p><p><br/></p><p><br/></p></body></html>"))
        self.label.setText(_translate("Dialog", "Motores paso a paso"))
        self.label_4.setText(_translate("Dialog", "INGRESE NUMERO DE VUELTAS"))
        self.pushButton.setText(_translate("Dialog", "INICIAR"))

    def start_motor(self):
        try:
            # Obtener el número de vueltas desde el `lineEdit`
            num_turns = float(self.lineEdit.text())
        except ValueError:
            # Si el valor no es válido, mostrar un mensaje y no hacer nada
            print("Ingrese un número válido de vueltas")
            return

        # Calcular el número total de pasos a realizar
        total_steps = int(num_turns * STEPS_PER_REVOLUTION)

        # Girar el motor por el número de pasos calculado
        for step in range(total_steps):
            for sequence in STEP_SEQUENCE:
                for pin in range(4):
                    GPIO.output(MOTOR_PINS[pin], sequence[pin])
                time.sleep(0.001)  # Ajustar para controlar la velocidad del motor

    def closeEvent(self, event):
        # Detener y limpiar los recursos de GPIO al cerrar
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
