from PyQt5 import QtCore, QtGui, QtWidgets
import math
import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from roboticstoolbox.backends.PyPlot import PyPlot
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import time

# Configuración de PCA9685
i2c = board.I2C()  # Usa board.SCL y board.SDA en la Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Frecuencia de servos

# Configuración de servos en los canales especificados
servos = {
    "base": servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2400),
    "shoulder": servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2400),
    "elbow": servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2400),
    "wrist": servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2400),
    "gripper": servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2400)
}

# Variables para invertir el giro de los servos si están instalados al revés
invert_direction = {
    "base": False,      # Cambia a True si el servo de la base está al revés
    "shoulder": False,  # Cambia a True si el servo del primer brazo está al revés
    "elbow": False,     # Cambia a True si el servo del segundo brazo está al revés
    "wrist": False,     # Cambia a True si el servo del tercer brazo está al revés
    "gripper": False    # Cambia a True si el gripper está al revés
}

# Offsets de 90 grados para servos en la posición inicial
offsets = {
    "shoulder": -90,  # La posición física de 90 grados se considera como 0 en la cinemática inversa
    "elbow": -90,
    "wrist": -90
}

# Longitudes ajustadas de los eslabones
d0 = 1.0   # Base que gira (longitud de 1)
d1 = 12.0  # Longitud del primer brazo
d2 = 12.0  # Longitud del segundo brazo
d3 = 11.0  # Longitud del tercer brazo (brazo final antes del gripper)

class Ui_Dialog(object):
    def __init__(self):
        self.robot = self.create_robot()
        self.simulation = PyPlot()
        self.simulation.launch()
        self.simulation.add(self.robot)

    def create_robot(self):
        # Crear articulaciones usando los parámetros de DH, según las longitudes correctas
        R = [
            RevoluteDH(d=d0, alpha=math.pi/2, a=0, offset=0),    # Base
            RevoluteDH(d=0, alpha=0, a=d1, offset=math.pi/2),    # Primer brazo
            RevoluteDH(d=0, alpha=0, a=d2, offset=0),            # Segundo brazo
            RevoluteDH(d=0, alpha=0, a=d3, offset=0)             # Tercer brazo
        ]
        robot = DHRobot(R, name='Bender')
        robot.q = [0, 0, 0, 0]
        return robot

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 450)
        
        # Labels y LineEdits para las coordenadas
        self.setup_coordinate_input(Dialog)
        
        # Botón para mover el robot
        self.pushButton_move = QtWidgets.QPushButton(Dialog)
        self.pushButton_move.setGeometry(QtCore.QRect(30, 130, 150, 30))
        self.pushButton_move.setText("Mover a Coordenadas")
        self.pushButton_move.clicked.connect(self.move_to_position)

        # Sliders para ángulos de cada articulación
        self.setup_sliders(Dialog)
        
        # Labels para mostrar ángulos calculados
        self.setup_angle_labels(Dialog)

    def setup_coordinate_input(self, Dialog):
        # Configura las entradas de coordenadas
        labels = ['X:', 'Y:', 'Z:']
        self.lineEdits = {}
        for i, label in enumerate(labels):
            lbl = QtWidgets.QLabel(Dialog)
            lbl.setGeometry(QtCore.QRect(30, 30 + 30 * i, 50, 20))
            lbl.setText(label)
            self.lineEdits[label] = QtWidgets.QLineEdit(Dialog)
            self.lineEdits[label].setGeometry(QtCore.QRect(80, 30 + 30 * i, 100, 20))

    def setup_sliders(self, Dialog):
        # Configura sliders de ángulos de cada articulación
        joints = ['Base', 'Shoulder', 'Elbow', 'Wrist']
        self.sliders = {}
        for i, joint in enumerate(joints):
            lbl = QtWidgets.QLabel(Dialog)
            lbl.setGeometry(QtCore.QRect(200, 30 + 30 * i, 50, 20))
            lbl.setText(f"{joint}:")
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, Dialog)
            slider.setGeometry(QtCore.QRect(250, 30 + 30 * i, 100, 20))
            slider.setMinimum(0)
            slider.setMaximum(180)
            slider.setValue(90)
            slider.valueChanged.connect(lambda _, j=joint.lower(): self.slider_changed(j))
            self.sliders[joint.lower()] = slider

    def setup_angle_labels(self, Dialog):
        # Configura las etiquetas para los ángulos calculados
        self.labels_angles = {}
        labels_text = ['Theta1:', 'Theta2:', 'Theta3:', 'Theta4:']
        for i, text in enumerate(labels_text):
            lbl = QtWidgets.QLabel(Dialog)
            lbl.setGeometry(QtCore.QRect(30, 170 + 30 * i, 100, 20))
            lbl.setText(text)
            self.labels_angles[text] = lbl

    def move_to_position(self):
        try:
            # Obtener valores de los campos de texto
            x = float(self.lineEdits['X:'].text()) if self.lineEdits['X:'].text() else 0.0
            y = float(self.lineEdits['Y:'].text()) if self.lineEdits['Y:'].text() else 0.0
            z = float(self.lineEdits['Z:'].text()) if self.lineEdits['Z:'].text() else 0.0
            
            # Calcular ángulos inversos (IK)
            theta1, theta2, theta3, theta4 = self.inverse_kinematics(x, y, z)
            
            # Asignar ángulos y actualizar la simulación
            self.robot.q = [np.radians(theta1), np.radians(theta2), np.radians(theta3), np.radians(theta4)]
            self.simulation.step()
            
            # Mover servos suavemente
            self.move_servos_smoothly(theta1, theta2, theta3, theta4)

        except ValueError:
            print("Error: Entrada no válida en los campos de posición.")

    def slider_changed(self, joint):
        angle = self.sliders[joint].value()
        # Sincronizar simulación y servos en tiempo real
        joint_angles = [self.sliders['base'].value(), self.sliders['shoulder'].value(),
                        self.sliders['elbow'].value(), self.sliders['wrist'].value()]
        self.robot.q = [np.radians(a) for a in joint_angles]
        self.simulation.step()
        # Mover servos correspondientes
        self.set_servo_angle(joint, angle)

    def inverse_kinematics(self, x, y, z):
        global d0, d1, d2, d3
        try:
            # Paso 1: Calcular theta1 (Rotación de la base)
            theta1 = math.atan2(y, x)

            # Paso 2: Calcular la distancia horizontal r y la altura s en el eje Z
            r = math.sqrt(x**2 + y**2)
            s = z - d0  # Restar la altura de la base

            # Paso 3: Calcular la distancia total d desde el origen al punto (x, y, z)
            d = math.sqrt(r**2 + s**2)

            # Verificar que el punto esté dentro del alcance del brazo
            if d > (d1 + d2 + d3):
                print("La posición está fuera del alcance del robot.")
                return 0, 0, 0, 0

            # Paso 4: Calcular theta3 usando la ley de cosenos
            cos_theta3 = (d**2 - d1**2 - d2**2) / (2 * d1 * d2)
            theta3 = math.acos(np.clip(cos_theta3, -1, 1))  # Ajustar el rango para evitar errores

            # Paso 5: Calcular theta2 considerando el efecto de theta3
            k1 = d1 + d2 * math.cos(theta3)
            k2 = d2 * math.sin(theta3)
            theta2 = math.atan2(s, r) - math.atan2(k2, k1)

            # Paso 6: Ajustar theta3 para la configuración física del robot
            theta3 = math.pi - theta3  # Invertir theta3 para adaptarlo a la geometría del brazo

            # Paso 7: Calcular theta4 para la orientación del efector final
            theta4 = 0  # Asumimos alineación horizontal del efector final

            # Convertir ángulos a grados
            theta1 = np.degrees(theta1)
            theta2 = np.degrees(theta2)
            theta3 = np.degrees(theta3)
            theta4 = np.degrees(theta4)

            # Aplicar offsets para ajustar la posición física a la posición lógica
            theta2 -= 90
            theta3 -= 90

            # Limitar los ángulos al rango de los servos (0 a 180 grados)
            theta1 = max(0, min(180, theta1))
            theta2 = max(0, min(180, theta2))
            theta3 = max(0, min(180, theta3))
            theta4 = max(0, min(180, theta4))

            return theta1, theta2, theta3, theta4

        except ValueError as e:
            print(f"Error en los cálculos de cinemática inversa: {e}")
            return 0, 0, 0, 0

    def set_servo_angle(self, servo_name, angle):
        # Invertir el ángulo si el servo está instalado al revés
        if invert_direction[servo_name]:
            angle = 180 - angle
        # Limitar el ángulo entre 0 y 180 grados y asignarlo al servo
        angle = max(0, min(180, angle))
        servos[servo_name].angle = angle

    def move_servos_smoothly(self, theta1, theta2, theta3, theta4, steps=50, delay=0.02):
        # Obtener los ángulos actuales de los servos
        current_angles = {
            "base": servos["base"].angle if servos["base"].angle is not None else 0,
            "shoulder": servos["shoulder"].angle if servos["shoulder"].angle is not None else 0,
            "elbow": servos["elbow"].angle if servos["elbow"].angle is not None else 0,
            "wrist": servos["wrist"].angle if servos["wrist"].angle is not None else 0
        }

        target_angles = {
            "base": theta1,
            "shoulder": theta2,
            "elbow": theta3,
            "wrist": theta4
        }

        # Mover los servos suavemente en pasos pequeños
        for step in range(steps + 1):
            for servo_name in ["base", "shoulder", "elbow", "wrist"]:
                # Calcular ángulo intermedio para cada servo
                intermediate_angle = current_angles[servo_name] + (target_angles[servo_name] - current_angles[servo_name]) * (step / steps)
                
                # Ajustar el ángulo del servo considerando la inversión
                self.set_servo_angle(servo_name, intermediate_angle)
                
                # Pequeña pausa para movimiento intercalado
                time.sleep(delay / len(servos))

            # Procesar eventos de Qt para mantener la UI activa
            QtWidgets.QApplication.processEvents()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())