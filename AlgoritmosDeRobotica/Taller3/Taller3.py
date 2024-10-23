from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import RPi.GPIO as GPIO
import time
from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np

# Configuración GPIO para Raspberry Pi
GPIO.setmode(GPIO.BCM)
SERVO1_PIN = 17  # Asigna un pin GPIO para el servo 1
SERVO2_PIN = 18  # Asigna un pin GPIO para el servo 2

GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

servo1 = GPIO.PWM(SERVO1_PIN, 50)  # Inicializa el servo 1 con una frecuencia de 50Hz
servo2 = GPIO.PWM(SERVO2_PIN, 50)  # Inicializa el servo 2 con una frecuencia de 50Hz
servo1.start(0)
servo2.start(0)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class Ui_Dialog(object):
    def __init__(self):
        self.robot = self.create_robot()

    def create_robot(self):
        # Configuración del robot SCARA con los parámetros DH
        link1 = RevoluteDH(d=0, a=1, alpha=0)
        link2 = RevoluteDH(d=0, a=1, alpha=0)
        return DHRobot([link1, link2], name='SCARA')

    def set_servo_angle(self, servo, angle):
        duty = angle / 18 + 2
        servo.ChangeDutyCycle(duty)
        time.sleep(1)  # Espera para que el movimiento se vea reflejado físicamente

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(860, 640)
        # Configuración de la interfaz gráfica
        self.graphicsView = QtWidgets.QWidget(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(450, 80, 256, 192))
        
        # Crear una figura de matplotlib dentro de graphicsView
        self.canvas = MplCanvas(self.graphicsView, width=5, height=4, dpi=100)
        layout = QtWidgets.QVBoxLayout(self.graphicsView)
        layout.addWidget(self.canvas)

        self.update_robot_graph(0, 0)

        # Aquí continúa la configuración de los elementos UI...
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 440, 261, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(450, 400, 271, 161))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../Taller2/logoUniversidadEcci.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(270, 10, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 60, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(150, 60, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 130, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 90, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 90, 113, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(150, 130, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(280, 130, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(450, 80, 256, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 80, 22))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 210, 80, 22))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 210, 80, 22))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 210, 80, 22))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 210, 80, 22))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(290, 240, 80, 22))
        self.pushButton_6.setObjectName("pushButton_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 240, 261, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 280, 80, 22))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.setGeometry(QtCore.QRect(110, 280, 80, 22))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Dialog)
        self.pushButton_9.setGeometry(QtCore.QRect(200, 280, 80, 22))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(Dialog)
        self.pushButton_10.setGeometry(QtCore.QRect(290, 280, 80, 22))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(Dialog)
        self.pushButton_11.setGeometry(QtCore.QRect(280, 90, 80, 22))
        self.pushButton_11.setObjectName("pushButton_11")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Conexiones de botones
        self.pushButton_11.clicked.connect(self.move_to_position)
        self.pushButton.clicked.connect(self.draw_yin_yang)

        # Asigna la función a los botones de nombres
        self.pushButton_2.clicked.connect(lambda: self.write_name("Felipe"))
        self.pushButton_3.clicked.connect(lambda: self.write_name("Jeisson"))
        self.pushButton_4.clicked.connect(lambda: self.write_name("Daniela"))
        self.pushButton_5.clicked.connect(lambda: self.write_name("William"))

        # Botón para escribir palabra ingresada en lineEdit_3
        self.pushButton_6.clicked.connect(self.write_custom_word)

        # Botones para logos (Ejemplo)
        self.pushButton_7.clicked.connect(lambda: self.draw_logo("Puma"))
        self.pushButton_8.clicked.connect(lambda: self.draw_logo("Toyota"))
        self.pushButton_9.clicked.connect(lambda: self.draw_logo("Apple"))
        self.pushButton_10.clicked.connect(lambda: self.draw_logo("Pepsi"))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">Daniela Rodriguez 83549</p><p align=\"center\">Jeison Sanchez   61849</p><p align=\"center\">Andres C. Rodriguez  83836</p><p align=\"center\">William A. Fernandez 77516</p><p><br/></p><p><br/></p></body></html>"))
        self.label.setText(_translate("Dialog", "Manejo de posiciones"))
        self.label_4.setText(_translate("Dialog", "Posicion x"))
        self.label_5.setText(_translate("Dialog", "Posicion Y"))
        self.label_6.setText(_translate("Dialog", "Angulo: X                     y"))
        self.label_7.setText(_translate("Dialog", "###"))
        self.label_8.setText(_translate("Dialog", "###"))
        self.pushButton.setText(_translate("Dialog", "Trayectoria"))
        self.pushButton_2.setText(_translate("Dialog", "Felipe"))
        self.pushButton_3.setText(_translate("Dialog", "Jeisson"))
        self.pushButton_4.setText(_translate("Dialog", "Daniela"))
        self.pushButton_5.setText(_translate("Dialog", "William"))
        self.pushButton_6.setText(_translate("Dialog", "Escribir"))
        self.pushButton_7.setText(_translate("Dialog", "Puma"))
        self.pushButton_8.setText(_translate("Dialog", "Toyota"))
        self.pushButton_9.setText(_translate("Dialog", "Apple"))
        self.pushButton_10.setText(_translate("Dialog", "Pepsi"))
        self.pushButton_11.setText(_translate("Dialog", "Mover"))

    def move_to_position(self):
        x = float(self.lineEdit.text())
        y = float(self.lineEdit_2.text())
        # Calcular ángulos inversos (IK) para alcanzar la posición (x, y)
        theta1, theta2 = self.inverse_kinematics(x, y)
        self.set_servo_angle(servo1, theta1)
        self.set_servo_angle(servo2, theta2)
        self.label_7.setText(f"{theta1:.2f}")
        self.label_8.setText(f"{theta2:.2f}")
        self.update_robot_graph(theta1, theta2)

    def inverse_kinematics(self, x, y):
        # Simulación del cálculo de ángulos inversos para el robot SCARA
        d1 = 1  # Longitud del primer brazo
        d2 = 1  # Longitud del segundo brazo
        theta2 = np.arccos((x**2 + y**2 - d1**2 - d2**2) / (2 * d1 * d2))
        theta1 = np.arctan2(y, x) - np.arctan2(d2 * np.sin(theta2), d1 + d2 * np.cos(theta2))
        return np.degrees(theta1), np.degrees(theta2)

    def draw_yin_yang(self):
        movements = [(0, 0), (90, 0), (180, 0), (180, 90), (0, 180), (0, 90), (0, 0)]
        for s1, s2 in movements:
            self.set_servo_angle(servo1, s1)
            self.set_servo_angle(servo2, s2)
            self.label_7.setText(f"{s1:.2f}")
            self.label_8.setText(f"{s2:.2f}")
            self.update_robot_graph(s1, s2)

    def write_name(self, name):
        # Lógica de escritura de nombre con el efector final
        # Podrías usar un método básico para cada letra en el nombre
        self.set_servo_angle(servo1, 45)
        self.set_servo_angle(servo2, 45)
        # (Completar la lógica de escritura)

    def write_custom_word(self):
        word = self.lineEdit_3.text()
        self.write_name(word)

    def draw_logo(self, logo_name):
        # Lógica para trazar los logos específicos
        self.set_servo_angle(servo1, 0)
        self.set_servo_angle(servo2, 0)
        time.sleep(2)  # Espera para que el usuario coloque el papel
        # (Implementar lógica para trazar el logo paso a paso)

    def update_robot_graph(self, theta1, theta2):
        # Dibujar el robot en el canvas de matplotlib
        self.canvas.axes.clear()
        # Calcular las posiciones del robot
        x1 = np.cos(np.radians(theta1))
        y1 = np.sin(np.radians(theta1))
        x2 = x1 + np.cos(np.radians(theta1 + theta2))
        y2 = y1 + np.sin(np.radians(theta1 + theta2))

        # Dibujar el robot SCARA
        self.canvas.axes.plot([0, x1, x2], [0, y1, y2], marker='o')
        self.canvas.axes.set_xlim(-2, 2)
        self.canvas.axes.set_ylim(-2, 2)
        self.canvas.axes.set_title("Simulación SCARA")
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
