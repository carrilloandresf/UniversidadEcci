from PyQt5 import QtCore, QtGui, QtWidgets
import time
from roboticstoolbox import DHRobot, RevoluteDH
from roboticstoolbox.backends.PyPlot import PyPlot
import numpy as np
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import math

# Configuración de PCA9685 y servos
i2c = board.I2C()  # usa board.SCL y board.SDA en la Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Configuración de frecuencia para servos

# Configuración de los servos en los canales 2 a 6
servo1 = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2400)
servo2 = servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2400)
servo3 = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2400)
servo4 = servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2400)
servo5 = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2400)

# Dimensiones del robot (ajustables)
d0 = 0 # Base
d1 = 12  # Longitud del primer brazo
d2 = 12  # Longitud del segundo brazo
d3 = 12  # 13 con gripper cerrado

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create robot instance
        self.robot = self.create_robot()
        self.simulation = PyPlot()  # Crear simulación de Peter Corke
        self.simulation.launch(limits=[-40, 40, -40, 40, -40, 40])  # Ajustar límites de la simulación
        self.simulation.add(self.robot)

        # Setup UI components
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 480, 151, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 80, 31, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 110, 31, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 140, 31, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 170, 31, 20))
        self.label_5.setObjectName("label_5")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 241, 191))
        self.groupBox.setObjectName("groupBox")

        # Create sliders and connect to servos
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(104, 80, 160, 16))
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(180)
        self.horizontalSlider.setValue(90)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(lambda value: self.slider_callback(servo5, 3, value))  # Base

        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(104, 110, 160, 16))
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setMaximum(180)
        self.horizontalSlider_2.setValue(90)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.valueChanged.connect(lambda value: self.slider_callback(servo4, 2, value))  # Primer brazo

        self.horizontalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(104, 140, 160, 16))
        self.horizontalSlider_3.setMinimum(0)
        self.horizontalSlider_3.setMaximum(180)
        self.horizontalSlider_3.setValue(90)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.valueChanged.connect(lambda value: self.slider_callback(servo3, 1, value))  # Segundo brazo

        self.horizontalSlider_4 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_4.setGeometry(QtCore.QRect(104, 170, 160, 16))
        self.horizontalSlider_4.setMinimum(0)
        self.horizontalSlider_4.setMaximum(180)
        self.horizontalSlider_4.setValue(90)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.valueChanged.connect(lambda value: self.slider_callback(servo2, 0, value))  # Tercer brazo

        self.horizontalSlider_5 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_5.setGeometry(QtCore.QRect(104, 200, 160, 16))
        self.horizontalSlider_5.setMinimum(0)
        self.horizontalSlider_5.setMaximum(180)
        self.horizontalSlider_5.setValue(90)
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName("horizontalSlider_5")
        self.horizontalSlider_5.valueChanged.connect(lambda value: self.slider_callback(servo1, None, value))  # Gripper

        # Additional UI components
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 280, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(70, 310, 21, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 340, 21, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(50, 450, 131, 91))
        self.label_9.setObjectName("label_9")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 280, 41, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 310, 41, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 340, 41, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 250, 161, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(330, 50, 211, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(60, 50, 80, 22))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 90, 80, 22))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(330, 220, 211, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(20, 30, 57, 14))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(20, 60, 57, 14))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(570, 70, 57, 14))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(60, 200, 31, 20))
        self.label_13.setObjectName("label_13")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Initialize servos to 90 degrees
        self.initialize_servos()

        # Connect button to start automatic mode
        self.pushButton.clicked.connect(self.start_automatic_mode)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Control de Robot"))
        self.label.setText(_translate("MainWindow", "Logo Ecci"))
        self.label_2.setText(_translate("MainWindow", "Art1"))
        self.label_3.setText(_translate("MainWindow", "Art2"))
        self.label_4.setText(_translate("MainWindow", "Art3"))
        self.label_5.setText(_translate("MainWindow", "Efec"))
        self.groupBox.setTitle(_translate("MainWindow", "Modo Manual"))
        self.label_6.setText(_translate("MainWindow", "x"))
        self.label_7.setText(_translate("MainWindow", "y"))
        self.label_8.setText(_translate("MainWindow", "z"))
        self.label_9.setText(_translate("MainWindow", "Presentado por:\n" "Andres Carrillo\n" "Daniela Rodriguez\n" "Jeisson Gutierrez\n" "William Fernandez"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Modo Semiautomatico"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Modo Automatico"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Sensores"))
        self.label_10.setText(_translate("MainWindow", "Sensor1"))
        self.label_11.setText(_translate("MainWindow", "Sensor2"))
        self.label_12.setText(_translate("MainWindow", "Alert"))
        self.label_13.setText(_translate("MainWindow", "Base"))

    def initialize_servos(self):
        # Inicializar servos y sliders a 90 grados
        for slider in [self.horizontalSlider, self.horizontalSlider_2, self.horizontalSlider_3, self.horizontalSlider_4, self.horizontalSlider_5]:						
            slider.setValue(90)														
        self.robot.q = [math.radians(90)] * 4
        self.update_simulation()

    def start_automatic_mode(self):
        # Move all servos to a specified position (e.g., 90 degrees)
        self.move_servos_smoothly(servo1, 90, joint_index=None)
        self.move_servos_smoothly(servo2, 90, joint_index=0)
        self.move_servos_smoothly(servo3, 90, joint_index=1)
        self.move_servos_smoothly(servo4, 90, joint_index=2)
        self.move_servos_smoothly(servo5, 90, joint_index=3)  # Efector final no tiene joint_index

    def slider_callback(self, servo_motor, joint_index, value):
        angle_radians = math.radians(value)  # Convertir a radianes para la simulación
        self.set_servo_angle(servo_motor, value, joint_index, angle_radians)

def update_simulation(self):
    if hasattr(self, 'simulation') and self.simulation:
        self.simulation.step(self.robot.q)



    def move_servos_smoothly(self, servo_motor, target_angle, joint_index=None, steps=20, delay=0.01):							 
        current_angle = servo_motor.angle if servo_motor.angle is not None else 90						   
        diff = target_angle - current_angle											  
        for step in range(steps + 1):
            intermediate_angle = current_angle + (diff / steps) * step
            angle_radians = math.radians(intermediate_angle)  # Para simulación
            self.set_servo_angle(servo_motor, intermediate_angle, joint_index, angle_radians)																		  
            time.sleep(delay)



    def set_servo_angle(self, servo_motor, angle, joint_index, angle_radians):											 
        angle = max(0, min(180, angle))
        servo_motor.angle = angle
        if joint_index is not None:														   
            angles = np.array(self.robot.q)													   
            angles[joint_index] = angle_radians						  
            self.robot.q = angles
            self.update_simulation()


    def create_robot(self):
        # Crear articulaciones usando los parámetros de DH
        R = [
            RevoluteDH(d=d0, alpha=math.pi/2, a=0, offset=0),
            RevoluteDH(d=0, alpha=0, a=d1, offset=math.pi/2),
            RevoluteDH(d=0, alpha=0, a=d2, offset=0),
            RevoluteDH(d=0, alpha=0, a=d3, offset=0)
        ]
        robot = DHRobot(R, name='Bender')
        robot.q = [0, 0, 0, 0]
        return robot

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())