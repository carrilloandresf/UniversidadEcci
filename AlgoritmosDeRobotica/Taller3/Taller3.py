from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import time
from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

# Configuración de PCA9685 y servos
i2c = board.I2C()  # usa board.SCL y board.SDA en la Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Configuración de frecuencia para servos

# Configuración de los servos en los canales 0 y 1
servo1 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2400)
servo2 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400)

class SimulationWindow(QMainWindow):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.setWindowTitle("Simulación del Robot")
        self.robot.teach(q=[0, 0])  # Abre la interfaz de visualización con la configuración inicial
        self.show()

    def update_graph(self, theta1, theta2):
        # Mueve el robot a los nuevos ángulos
        self.robot.q = [np.radians(theta1), np.radians(theta2)]
        # Refrescar la visualización
        self.robot.teach(q=self.robot.q)

class Ui_MainWindow:
    def __init__(self):
        # Creación del robot y ventana de simulación
        self.robot = self.create_robot()
        self.simulation_window = SimulationWindow(self.robot)  # Ventana de simulación

    def create_robot(self):
        link1 = RevoluteDH(d=0, a=1, alpha=0)
        link2 = RevoluteDH(d=0, a=1, alpha=0)
        return DHRobot([link1, link2], name='ROBOT')

    def set_servo_angle(self, servo_motor, angle):
        angle = max(0, min(180, angle))
        servo_motor.angle = angle

    def move_servos_smoothly(self, target_angle1, target_angle2, steps=100, delay=0.01):
        current_angle1 = servo1.angle if servo1.angle is not None else 0
        current_angle2 = servo2.angle if servo2.angle is not None else 0
        diff1 = target_angle1 - current_angle1
        diff2 = target_angle2 - current_angle2
        for step in range(steps + 1):
            intermediate_angle1 = current_angle1 + (diff1 / steps) * step
            intermediate_angle2 = current_angle2 + (diff2 / steps) * step
            self.set_servo_angle(servo1, intermediate_angle1)
            self.set_servo_angle(servo2, intermediate_angle2)
            self.label_7.setText(f"{intermediate_angle1:.2f}")
            self.label_8.setText(f"{intermediate_angle2:.2f}")
            self.simulation_window.update_graph(intermediate_angle1, intermediate_angle2)
            QtWidgets.QApplication.processEvents()
            time.sleep(delay)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Configuración de los elementos UI
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 440, 261, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(450, 400, 271, 161))
        self.label_3.setPixmap(QtGui.QPixmap("../Taller2/logoUniversidadEcci.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 10, 291, 41))
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 60, 291, 41))
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(150, 60, 291, 41))
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 130, 291, 41))
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 90, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 90, 113, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(150, 130, 81, 41))
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(280, 130, 81, 41))
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 80, 22))
        self.pushButton.setObjectName("pushButton")
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulación Robot"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Daniela Rodriguez 83549</p><p align=\"center\">Jeison Sanchez 61849</p><p align=\"center\">Andres C. Rodriguez 83836</p><p align=\"center\">William A. Fernandez 77516</p><p><br/></p><p><br/></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Manejo de posiciones"))
        self.label_4.setText(_translate("MainWindow", "Posición X"))
        self.label_5.setText(_translate("MainWindow", "Posición Y"))
        self.label_6.setText(_translate("MainWindow", "Ángulo S1 y S2"))
        self.label_7.setText(_translate("MainWindow", "###"))
        self.label_8.setText(_translate("MainWindow", "###"))
        self.pushButton.setText(_translate("MainWindow", "Trayectoria"))

    def move_to_position(self):
        print("move_to_position")                                 
        x = float(self.lineEdit.text())
        y = float(self.lineEdit_2.text())
        # Calcular ángulos inversos (IK) para alcanzar la posición (x, y)
        theta1, theta2 = self.inverse_kinematics(x, y)
        self.label_7.setText(f"{theta1:.2f}")
        self.label_8.setText(f"{theta2:.2f}")
        self.simulation_window.update_graph(theta1, theta2)
        self.move_servos_smoothly(theta1, theta2)  # Mover suavemente ambos servos

    def inverse_kinematics(self, x, y):
        # Longitudes de los eslabones
        d1 = 1  # Longitud del primer brazo
        d2 = 0.5  # Longitud del segundo brazo

        # Calcular el valor del coseno de theta2, asegurando que esté en el rango [-1, 1]
        cos_theta2 = (x**2 + y**2 - d1**2 - d2**2) / (2 * d1 * d2)
        cos_theta2 = np.clip(cos_theta2, -1, 1)

        try:
            # Calcular theta2 en radianes (dos posibles soluciones)
            theta2_rad = np.arccos(cos_theta2)
            k1 = d1 + d2 * np.cos(theta2_rad)
            k2 = d2 * np.sin(theta2_rad)
            theta1_rad = np.arctan2(y, x) - np.arctan2(k2, k1)
            theta1 = np.degrees(theta1_rad)
            theta2 = np.degrees(theta2_rad)

            theta1 = (theta1 + 360) % 360
            if theta1 > 180:
                theta1 -= 360
            theta1 = max(0, min(180, theta1))
            theta2 = max(0, min(180, theta2))

            return theta1, theta2
        except ValueError:
            print("Error en los cálculos de cinemática inversa: valores fuera de rango.")
            return 0, 0

    def draw_yin_yang(self):
        movements = [(0, 0), (90, 0), (180, 0), (180, 90), (180, 180), (0, 180), (0, 90), (0, 0)]
        for s1, s2 in movements:
            theta1, theta2 = s1, s2
            self.simulation_window.update_graph(theta1, theta2)
            self.label_8.setText(f"{theta2:.2f}")
            self.label_7.setText(f"{theta1:.2f}")
            self.move_servos_smoothly(theta1, theta2)
            time.sleep(1)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())