# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO

# Pines GPIO para los LEDs
LED_1 = 27  # LED controlado por `pushButton` y `servomotor1` (PWM)
LED_2 = 5   # LED controlado por `pushButton_2` y `servomotor2` (PWM)

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)

# Configuración de PWM para los LEDs
pwm_led1 = GPIO.PWM(LED_1, 1000)  # 1000 Hz de frecuencia
pwm_led2 = GPIO.PWM(LED_2, 1000)

pwm_led1.start(0)
pwm_led2.start(0)

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

        # Slider para ajustar el brillo del LED 1
        self.servomotor1 = QtWidgets.QSlider(Dialog)
        self.servomotor1.setGeometry(QtCore.QRect(150, 210, 160, 22))
        self.servomotor1.setMaximum(100)
        self.servomotor1.setOrientation(QtCore.Qt.Horizontal)
        self.servomotor1.setObjectName("servomotor1")

        # Slider para ajustar el brillo del LED 2
        self.servomotor2 = QtWidgets.QSlider(Dialog)
        self.servomotor2.setGeometry(QtCore.QRect(430, 210, 160, 22))
        self.servomotor2.setMaximum(100)
        self.servomotor2.setTracking(True)
        self.servomotor2.setOrientation(QtCore.Qt.Horizontal)
        self.servomotor2.setInvertedAppearance(False)
        self.servomotor2.setObjectName("servomotor2")

        # Etiquetas para mostrar el porcentaje de brillo
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(160, 260, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(440, 260, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        # Botones para encender y apagar LEDs
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 80, 121, 41))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 80, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(270, 10, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conectar eventos
        self.pushButton.clicked.connect(self.toggle_led1)
        self.pushButton_2.clicked.connect(self.toggle_led2)
        self.servomotor1.valueChanged.connect(self.adjust_brightness_led1)
        self.servomotor2.valueChanged.connect(self.adjust_brightness_led2)

        # Estado inicial de los LEDs (apagados)
        self.led1_state = False
        self.led2_state = False

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Control de LEDs"))
        self.label_2.setText(_translate("Dialog", "Andrés Felipe Carrillo Rodríguez\n"
"Daniela Rodríguez Pelaez\n"
"Jeisson Gutierrez Sanchez\n"
"William Alejandro Fernandez Pinzón\n"
"Ingeniería Mecatrónica\n"
"Electiva de Robótica\n"
"2024 - II"))
        self.label_4.setText(_translate("Dialog", "Intensidad LED 1: 0%"))
        self.label_5.setText(_translate("Dialog", "Intensidad LED 2: 0%"))
        self.pushButton.setText(_translate("Dialog", "LED VERDE"))
        self.pushButton_2.setText(_translate("Dialog", "LED ROJO"))
        self.label.setText(_translate("Dialog", "Escritura de puertos"))

    def toggle_led1(self):
        # Cambiar el estado del LED 1 (encendido/apagado)
        self.led1_state = not self.led1_state
        if self.led1_state:
            pwm_led1.ChangeDutyCycle(self.servomotor1.value())  # Ajustar brillo según el slider
        else:
            pwm_led1.ChangeDutyCycle(0)
        # Cambiar color del botón
        self.pushButton.setStyleSheet("background-color: green" if self.led1_state else "background-color: none")

    def toggle_led2(self):
        # Cambiar el estado del LED 2 (encendido/apagado)
        self.led2_state = not self.led2_state
        if self.led2_state:
            pwm_led2.ChangeDutyCycle(self.servomotor2.value())  # Ajustar brillo según el slider
        else:
            pwm_led2.ChangeDutyCycle(0)
        # Cambiar color del botón
        self.pushButton_2.setStyleSheet("background-color: red" if self.led2_state else "background-color: none")

    def adjust_brightness_led1(self, value):
        # Ajustar el brillo del LED 1 y mostrar el porcentaje en `label_4`
        if self.led1_state:  # Solo ajustar brillo si el LED está encendido
            pwm_led1.ChangeDutyCycle(value)
        self.label_4.setText(f"Intensidad LED 1: {value}%")

    def adjust_brightness_led2(self, value):
        # Ajustar el brillo del LED 2 y mostrar el porcentaje en `label_5`
        if self.led2_state:  # Solo ajustar brillo si el LED está encendido
            pwm_led2.ChangeDutyCycle(value)
        self.label_5.setText(f"Intensidad LED 2: {value}%")

    def closeEvent(self, event):
        # Detener y limpiar los recursos de GPIO
        pwm_led1.stop()
        pwm_led2.stop()
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
