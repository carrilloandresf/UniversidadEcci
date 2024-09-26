# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO
import time

# Pines BCM para los servos
SERVO_1 = 13
SERVO_2 = 16

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_1, GPIO.OUT)
GPIO.setup(SERVO_2, GPIO.OUT)

# Configurar PWM para los servomotores
pwm_servo1 = GPIO.PWM(SERVO_1, 50)  # 50 Hz
pwm_servo2 = GPIO.PWM(SERVO_2, 50)  # 50 Hz

pwm_servo1.start(0)
pwm_servo2.start(0)

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
        self.label_3.setPixmap(QtGui.QPixmap("../../src/img/logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        
        # Slider para controlar el ángulo del servomotor seleccionado
        self.servomotor_slider = QtWidgets.QSlider(Dialog)
        self.servomotor_slider.setGeometry(QtCore.QRect(150, 210, 160, 22))
        self.servomotor_slider.setMaximum(180)
        self.servomotor_slider.setOrientation(QtCore.Qt.Horizontal)
        self.servomotor_slider.setObjectName("servomotor_slider")

        # Campo de texto para seleccionar el servomotor
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(320, 30, 131, 51))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        # Label para mostrar el ángulo actual
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 160, 81, 41))
        self.label.setObjectName("label")

        # Botón para actualizar la selección del servomotor
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(320, 90, 131, 51))
        self.pushButton.setObjectName("pushButton")

        # Label para mostrar cuál slider está siendo controlado
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(160, 260, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        # Label para mostrar el ángulo actual del servomotor
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(280, 320, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conectar eventos
        self.pushButton.clicked.connect(self.update_servo_selection)
        self.servomotor_slider.valueChanged.connect(self.move_servo)

        # Variable para almacenar el servomotor seleccionado (1 o 2)
        self.selected_servo = 1

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Control de Servomotores"))
        self.label_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Andrés Felipe Carrillo Rodríguez<br>\n"
"Daniela Rodríguez Pelaez<br>\n"
"Jeisson Gutierrez Sanchez<br>\n"
"William Alejandro Fernandez Pinzón</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ingeniería Mecatrónica<br>\n"
"Electiva de Robótica<br>\n"
"2024 - II</p></body></html>"))
        self.label.setText(_translate("Dialog", "Ángulo"))
        self.pushButton.setText(_translate("Dialog", "Actualizar Servo"))
        self.label_4.setText(_translate("Dialog", "Servo Seleccionado: 1"))
        self.label_7.setText(_translate("Dialog", "Ángulo Actual: 0°"))

    def update_servo_selection(self):
        # Verificar el valor en el lineEdit para seleccionar el servomotor
        try:
            number = int(self.lineEdit.text())
            if number % 2 == 0:
                self.selected_servo = 2
                self.label_4.setText("Servo Seleccionado: 2")
            else:
                self.selected_servo = 1
                self.label_4.setText("Servo Seleccionado: 1")
        except ValueError:
            # Si el valor no es un número, mantener el servo actual
            self.label_4.setText("Valor no válido, servo actual: {}".format(self.selected_servo))

    def move_servo(self):
        # Obtener el ángulo del slider
        angle = self.servomotor_slider.value()
        duty_cycle = 2 + (angle / 18.0)  # Calcular el ciclo de trabajo para el ángulo
        self.label_7.setText(f"Ángulo Actual: {angle}°")

        # Mover el servomotor seleccionado
        if self.selected_servo == 1:
            pwm_servo1.ChangeDutyCycle(duty_cycle)
        else:
            pwm_servo2.ChangeDutyCycle(duty_cycle)
        
        time.sleep(0.02)  # Pequeña pausa para asegurar el movimiento
        GPIO.output(SERVO_1, False)
        GPIO.output(SERVO_2, False)

    def closeEvent(self, event):
        # Detener y limpiar los recursos de GPIO
        pwm_servo1.stop()
        pwm_servo2.stop()
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
