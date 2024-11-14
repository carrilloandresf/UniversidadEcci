from PyQt5 import QtCore, QtGui, QtWidgets
import time
from roboticstoolbox import DHRobot, RevoluteDH
from roboticstoolbox.backends.PyPlot import PyPlot
import numpy as np
import board
import sys
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import math
import os

# Configurar variable de entorno para omitir advertencias de Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"  # Fuerza el uso de X11 en lugar de Wayland

# Configuración de PCA9685 y servos
i2c = board.I2C()  # Usa board.SCL y board.SDA en la Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Configuración de frecuencia para servos

# Configuración de los servos en los canales correspondientes
servo_base = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2400)   # Base rotativa
servo_shoulder = servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2400)  # Hombro
servo_elbow = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2400)   # Codo
servo_wrist = servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2400)   # Muñeca
servo_gripper = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2400)  # Efector final (pinza)

# Dimensiones del robot (ajustables según tu robot real)
d1 = 1.0   # Longitud del primer eslabón (hombro)
d2 = 1.0   # Longitud del segundo eslabón (codo)
d3 = 0.5   # Longitud del tercer eslabón (muñeca)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Control de Robot")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Crear instancia del robot
        self.robot = self.create_robot()
        self.simulation = PyPlot()
        self.simulation.launch(limits=[-3, 3, -3, 3, -0.5, 3])  # Ajustar límites según sea necesario
        self.simulation.add(self.robot)

        # Configuración de los componentes de la interfaz
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 30, 300, 250))
        self.groupBox.setTitle("Control Manual")

        # Labels para los sliders
        self.label_base = QtWidgets.QLabel(self.groupBox)
        self.label_base.setGeometry(QtCore.QRect(10, 30, 60, 20))
        self.label_base.setText("Base")

        self.label_shoulder = QtWidgets.QLabel(self.groupBox)
        self.label_shoulder.setGeometry(QtCore.QRect(10, 70, 60, 20))
        self.label_shoulder.setText("Hombro")

        self.label_elbow = QtWidgets.QLabel(self.groupBox)
        self.label_elbow.setGeometry(QtCore.QRect(10, 110, 60, 20))
        self.label_elbow.setText("Codo")

        self.label_wrist = QtWidgets.QLabel(self.groupBox)
        self.label_wrist.setGeometry(QtCore.QRect(10, 150, 60, 20))
        self.label_wrist.setText("Muñeca")

        self.label_gripper = QtWidgets.QLabel(self.groupBox)
        self.label_gripper.setGeometry(QtCore.QRect(10, 190, 60, 20))
        self.label_gripper.setText("Pinza")

        # Sliders para controlar los servos
        self.slider_base = QtWidgets.QSlider(self.groupBox)
        self.slider_base.setGeometry(QtCore.QRect(80, 30, 200, 20))
        self.slider_base.setMinimum(0)
        self.slider_base.setMaximum(180)
        self.slider_base.setValue(90)
        self.slider_base.setOrientation(QtCore.Qt.Horizontal)
        self.slider_base.valueChanged.connect(lambda value: self.slider_callback(servo_base, 0, value))

        self.slider_shoulder = QtWidgets.QSlider(self.groupBox)
        self.slider_shoulder.setGeometry(QtCore.QRect(80, 70, 200, 20))
        self.slider_shoulder.setMinimum(0)
        self.slider_shoulder.setMaximum(180)
        self.slider_shoulder.setValue(90)
        self.slider_shoulder.setOrientation(QtCore.Qt.Horizontal)
        self.slider_shoulder.valueChanged.connect(lambda value: self.slider_callback(servo_shoulder, 1, value))

        self.slider_elbow = QtWidgets.QSlider(self.groupBox)
        self.slider_elbow.setGeometry(QtCore.QRect(80, 110, 200, 20))
        self.slider_elbow.setMinimum(0)
        self.slider_elbow.setMaximum(180)
        self.slider_elbow.setValue(90)
        self.slider_elbow.setOrientation(QtCore.Qt.Horizontal)
        self.slider_elbow.valueChanged.connect(lambda value: self.slider_callback(servo_elbow, 2, value))

        self.slider_wrist = QtWidgets.QSlider(self.groupBox)
        self.slider_wrist.setGeometry(QtCore.QRect(80, 150, 200, 20))
        self.slider_wrist.setMinimum(0)
        self.slider_wrist.setMaximum(180)
        self.slider_wrist.setValue(90)
        self.slider_wrist.setOrientation(QtCore.Qt.Horizontal)
        self.slider_wrist.valueChanged.connect(lambda value: self.slider_callback(servo_wrist, 3, value))

        self.slider_gripper = QtWidgets.QSlider(self.groupBox)
        self.slider_gripper.setGeometry(QtCore.QRect(80, 190, 200, 20))
        self.slider_gripper.setMinimum(0)
        self.slider_gripper.setMaximum(180)
        self.slider_gripper.setValue(90)
        self.slider_gripper.setOrientation(QtCore.Qt.Horizontal)
        self.slider_gripper.valueChanged.connect(lambda value: self.slider_callback(servo_gripper, None, value))

        # Botón para posición inicial
        self.btn_home = QtWidgets.QPushButton(self.centralwidget)
        self.btn_home.setGeometry(QtCore.QRect(30, 300, 120, 30))
        self.btn_home.setText("Posición Inicial")
        self.btn_home.clicked.connect(self.move_to_home)

        # Botón para ejecutar movimiento automático (ejemplo)
        self.btn_automatic = QtWidgets.QPushButton(self.centralwidget)
        self.btn_automatic.setGeometry(QtCore.QRect(160, 300, 120, 30))
        self.btn_automatic.setText("Movimiento Automático")
        self.btn_automatic.clicked.connect(self.start_automatic_movement)

        MainWindow.setCentralWidget(self.centralwidget)

        # Inicializar servos y simulación
        self.initialize_servos()

    def initialize_servos(self):
        # Establecer los servos físicos en 90 grados
        self.set_servo_angle(servo_base, 90)
        self.set_servo_angle(servo_shoulder, 90)
        self.set_servo_angle(servo_elbow, 90)
        self.set_servo_angle(servo_wrist, 90)
        self.set_servo_angle(servo_gripper, 90)

        # Establecer los sliders en 90 grados
        self.slider_base.blockSignals(True)
        self.slider_shoulder.blockSignals(True)
        self.slider_elbow.blockSignals(True)
        self.slider_wrist.blockSignals(True)
        self.slider_gripper.blockSignals(True)

        self.slider_base.setValue(90)
        self.slider_shoulder.setValue(90)
        self.slider_elbow.setValue(90)
        self.slider_wrist.setValue(90)
        self.slider_gripper.setValue(90)

        self.slider_base.blockSignals(False)
        self.slider_shoulder.blockSignals(False)
        self.slider_elbow.blockSignals(False)
        self.slider_wrist.blockSignals(False)
        self.slider_gripper.blockSignals(False)

        # Actualizar la simulación con las posiciones iniciales
        self.robot.q = [0, 0, 0, 0]  # Ángulos iniciales en radianes
        self.simulation.draw(self.robot.q)

    def slider_callback(self, servo_motor, joint_index, value):
        # Mover el servo al ángulo especificado
        self.move_servo(servo_motor, value, joint_index)

    def move_servo(self, servo_motor, target_angle, joint_index=None):
        # Bloquear señales del slider para evitar bucles infinitos
        if joint_index is not None:
            slider = self.get_slider_by_joint_index(joint_index)
            if slider:
                slider.blockSignals(True)

        # Establecer el ángulo del servo
        self.set_servo_angle(servo_motor, target_angle)

        # Actualizar la simulación
        if joint_index is not None:
            self.update_simulation(joint_index, target_angle)

        # Desbloquear señales del slider
        if joint_index is not None:
            if slider:
                slider.blockSignals(False)

    def set_servo_angle(self, servo_motor, angle):
        # Limitar el ángulo entre 0 y 180 grados
        angle = max(0, min(180, angle))
        servo_motor.angle = angle

    def update_simulation(self, joint_index, angle):
        # Actualizar la simulación del robot
        if hasattr(self, 'robot'):
            if joint_index is not None and 0 <= joint_index < len(self.robot.q):
                q = self.robot.q.copy()
                # Ajustar el ángulo para que coincida con la orientación de la simulación
                adjusted_angle = math.radians(angle - 90)
                q[joint_index] = adjusted_angle
                self.robot.q = q
                if hasattr(self, 'simulation') and self.simulation:
                    self.simulation.draw(q=self.robot.q)

    def get_slider_by_joint_index(self, joint_index):
        # Retornar el slider correspondiente al índice de la articulación
        if joint_index == 0:
            return self.slider_base
        elif joint_index == 1:
            return self.slider_shoulder
        elif joint_index == 2:
            return self.slider_elbow
        elif joint_index == 3:
            return self.slider_wrist
        else:
            return None

    def create_robot(self):
        # Definir los parámetros DH para representar correctamente el robot

        # Articulación 1: Base rotativa (rotación alrededor del eje Z)
        link1 = RevoluteDH(d=0, a=0, alpha=0)

        # Articulación 2: Hombro (rotación alrededor del eje Y)
        link2 = RevoluteDH(d=0, a=0, alpha=-np.pi/2)

        # Articulación 3: Codo (rotación alrededor del eje Y)
        link3 = RevoluteDH(d=0, a=d2, alpha=0)

        # Articulación 4: Muñeca (rotación alrededor del eje Y)
        link4 = RevoluteDH(d=0, a=d3, alpha=0)

        robot = DHRobot([link1, link2, link3, link4], name='4DOF_ROBOT')
        robot.q = [0, 0, 0, 0]  # Configuración inicial en radianes
        return robot

    def move_to_home(self):
        # Mover el robot a la posición inicial
        self.move_servo(servo_base, 90, 0)
        self.move_servo(servo_shoulder, 90, 1)
        self.move_servo(servo_elbow, 90, 2)
        self.move_servo(servo_wrist, 90, 3)
        self.move_servo(servo_gripper, 90, None)

    def start_automatic_movement(self):
        # Ejemplo de movimiento automático (puedes personalizarlo)
        # Aquí realizaremos un movimiento simple para demostrar

        # Lista de posiciones (ángulos en grados) para cada articulación
        positions = [
            (90, 90, 90, 90),
            (90, 60, 120, 90),
            (90, 120, 60, 90),
            (90, 90, 90, 90)
        ]

        for pos in positions:
            # Mover cada articulación a la posición especificada
            self.move_servo(servo_base, pos[0], 0)
            self.move_servo(servo_shoulder, pos[1], 1)
            self.move_servo(servo_elbow, pos[2], 2)
            self.move_servo(servo_wrist, pos[3], 3)
            time.sleep(1)  # Esperar un segundo entre movimientos

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Control de Robot"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())