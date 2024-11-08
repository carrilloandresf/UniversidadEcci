from PyQt5 import QtCore, QtGui, QtWidgets
import time
from roboticstoolbox import DHRobot, RevoluteDH
from roboticstoolbox.backends.PyPlot import PyPlot
import numpy as np
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import os

# Configurar variable de entorno para omitir advertencias de Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"  # Fuerza el uso de X11 en lugar de Wayland

# Configuración de PCA9685 y servos
i2c = board.I2C()  # usa board.SCL y board.SDA en la Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Configuración de frecuencia para servos

# Configuración de los servos en los canales 0 y 1
servo1 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2400)  # Consider moving min_pulse and max_pulse values to configurable variables or constants
servo2 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400)

# Dimensiones del robot (ajustables)
d1 = 1.0  # Longitud del primer brazo
d2 = 0.5  # Longitud del segundo brazo

class Ui_Dialog(object):
    def __init__(self):
        self.robot = self.create_robot()
        self.simulation = PyPlot()  # Crear simulación de Peter Corke
        self.simulation.launch()
        self.simulation.add(self.robot)

    def create_robot(self):
        link1 = RevoluteDH(d=0, a=d1, alpha=0)
        link2 = RevoluteDH(d=0, a=d2, alpha=0)
        return DHRobot([link1, link2], name='ROBOT')

    def set_servo_angle(self, servo_motor, angle):
        # Limitar el ángulo entre 0 y 180 grados
        angle = max(0, min(180, angle))
        servo_motor.angle = angle

    def move_servos_smoothly(self, target_angle1, target_angle2, steps=100, delay=0.01):
        # Validar que 'steps' sea un entero positivo
        if steps <= 0:
            raise ValueError("Steps must be a positive integer")

        # Obtener los ángulos actuales de los servos
        current_angle1 = servo1.angle if servo1.angle is not None else 0
        current_angle2 = servo2.angle if servo2.angle is not None else 0

        # Calcular las diferencias de ángulo
        diff1 = target_angle1 - current_angle1
        diff2 = target_angle2 - current_angle2

        # Mover en pequeños pasos para hacer el movimiento más suave
        for step in range(steps + 1):
            # Calcular los ángulos intermedios para ambos servos
            intermediate_angle1 = current_angle1 + (diff1 / steps) * step
            intermediate_angle2 = current_angle2 + (diff2 / steps) * step

            # Establecer los ángulos intermedios para ambos servos
            self.set_servo_angle(servo1, intermediate_angle1)
            self.set_servo_angle(servo2, intermediate_angle2)

            # Actualizar la simulación del robot
            if step % 10 == 0:  # Reduce la frecuencia de actualización para mejorar el rendimiento
                self.robot.q = [np.radians(intermediate_angle1), np.radians(intermediate_angle2)]
                self.simulation.step()

            # Actualizar los labels con los valores actuales
            if step % 10 == 0:  # Actualizar menos frecuentemente para mejorar el rendimiento
                self.label_7.setText(f"{intermediate_angle1:.2f}")
                self.label_8.setText(f"{intermediate_angle2:.2f}")

            # Permitir que Qt procese eventos pendientes para actualizar la UI
            QtWidgets.QApplication.processEvents()

            # Consider using QTimer for delays to avoid blocking the UI thread
            time.sleep(delay)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(860, 640)
        # Configuración de los elementos UI
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
        self.label_6.setText(_translate("Dialog", "Angulo:S1                S2"))
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
        print("move_to_position")                                 
        # Verificar si los campos están vacíos y asignar valores predeterminados
        try:
            x = float(self.lineEdit.text()) if self.lineEdit.text() else 0.0
            y = float(self.lineEdit_2.text()) if self.lineEdit_2.text() else 0.0
        except ValueError:
            print("Error: Entrada no válida en los campos de posición.")
            return

        # Calcular ángulos inversos (IK) para alcanzar la posición (x, y)
        theta1, theta2 = self.inverse_kinematics(x, y)
        self.label_7.setText(f"{theta1:.2f}")
        self.label_8.setText(f"{theta2:.2f}")
        self.move_servos_smoothly(theta1, theta2)  # Mover suavemente ambos servos

    def inverse_kinematics(self, x, y):
        # Longitudes de los eslabones (ajustables)
        global d1, d2

        # Calcular el valor del coseno de theta2, asegurando que esté en el rango [-1, 1]
        cos_theta2 = (x**2 + y**2 - d1**2 - d2**2) / (2 * d1 * d2)

        # Limitar el valor de cos_theta2 para evitar errores de dominio
        cos_theta2 = np.clip(cos_theta2, -1, 1)

        try:
            # Calcular theta2 en radianes (hay dos posibles soluciones, se puede usar la que mejor se adapte)
            theta2_rad = np.arccos(cos_theta2)

            # Calcular theta1 considerando las dos soluciones posibles
            k1 = d1 + d2 * np.cos(theta2_rad)
            k2 = d2 * np.sin(theta2_rad)
            theta1_rad = np.arctan2(y, x) - np.arctan2(k2, k1)

            # Convertir ángulos a grados
            theta1 = np.degrees(theta1_rad)
            theta2 = np.degrees(theta2_rad)

            # Ajustar los ángulos al rango de 0 a 180 grados para que los servos puedan manejarlos
            theta1 = (theta1 + 360) % 360  # Asegurar que esté en rango positivo
            if theta1 > 180:
                theta1 -= 360

            # Limitar theta1 y theta2 al rango de trabajo del servo (0 a 180 grados)
            theta1 = max(0, min(180, theta1))
            theta2 = max(0, min(180, theta2))

            return theta1, theta2
        except ValueError:
            # Si hay un error, retornar ángulos predeterminados o levantar una excepción
            print("Error en los cálculos de cinemática inversa: valores fuera de rango.")
            return 0, 0

    def draw_yin_yang(self):
        print("draw_yin_yang")
        movements = [(0, 0), (90, 0), (180, 0), (180, 90), (180, 180), (0, 180), (0, 90), (0, 0)]
        
        for s1, s2 in movements:
            print(s1, "|", s2)
            theta1, theta2 = s1, s2
            self.move_servos_smoothly(theta1, theta2)

            # Esperar un segundo antes de pasar al siguiente movimiento
            time.sleep(1)

    def write_name(self, name):
        print("Iniciando escritura del nombre: ", name)

        # Configuración inicial del punto de partida
        start_x = -1.0
        start_y = 0.5

        # Mover el efector al punto de inicio antes de comenzar a escribir
        print(f"Moviendo al punto de inicio: ({start_x}, {start_y})")
        theta1, theta2 = self.inverse_kinematics(start_x, start_y)
        self.move_servos_smoothly(theta1, theta2)
        time.sleep(0.5)

        # Diccionario con la representación simplificada de cada letra usando puntos en el plano cartesiano (x, y)
        alphabet_points = {
            'A': [(0.1, 0.2), (0.2, 0.5), (0.3, 0.2), (0.2, 0.35)],
            'B': [(0.1, 0.2), (0.1, 0.5), (0.25, 0.4), (0.1, 0.35), (0.25, 0.3), (0.1, 0.2)],
            'C': [(0.3, 0.5), (0.1, 0.5), (0.1, 0.2), (0.3, 0.2)],
            'D': [(0.1, 0.2), (0.1, 0.5), (0.25, 0.4), (0.25, 0.3), (0.1, 0.2)],
            'E': [(0.3, 0.5), (0.1, 0.5), (0.1, 0.35), (0.2, 0.35), (0.1, 0.35), (0.1, 0.2), (0.3, 0.2)],
            'F': [(0.3, 0.5), (0.1, 0.5), (0.1, 0.35), (0.2, 0.35), (0.1, 0.35), (0.1, 0.2)],
            'G': [(0.3, 0.5), (0.1, 0.5), (0.1, 0.2), (0.3, 0.2), (0.3, 0.35)],
            'H': [(0.1, 0.5), (0.1, 0.2), (0.1, 0.35), (0.3, 0.35), (0.3, 0.5), (0.3, 0.2)],
            'I': [(0.2, 0.5), (0.2, 0.2)],
            'J': [(0.3, 0.5), (0.3, 0.2), (0.2, 0.2), (0.1, 0.3)],
            'K': [(0.1, 0.5), (0.1, 0.2), (0.1, 0.35), (0.3, 0.5), (0.1, 0.35), (0.3, 0.2)],
            'L': [(0.1, 0.5), (0.1, 0.2), (0.3, 0.2)],
            'M': [(0.1, 0.2), (0.1, 0.5), (0.2, 0.35), (0.3, 0.5), (0.3, 0.2)],
            'N': [(0.1, 0.2), (0.1, 0.5), (0.3, 0.2), (0.3, 0.5)],
            'O': [(0.2, 0.5), (0.1, 0.4), (0.1, 0.3), (0.2, 0.2), (0.3, 0.3), (0.3, 0.4), (0.2, 0.5)],
            'P': [(0.1, 0.2), (0.1, 0.5), (0.25, 0.5), (0.25, 0.35), (0.1, 0.35)],
            'Q': [(0.2, 0.5), (0.1, 0.4), (0.1, 0.3), (0.2, 0.2), (0.3, 0.3), (0.3, 0.4), (0.2, 0.5), (0.3, 0.2)],
            'R': [(0.1, 0.2), (0.1, 0.5), (0.25, 0.5), (0.25, 0.35), (0.1, 0.35), (0.3, 0.2)],
            'S': [(0.3, 0.5), (0.1, 0.5), (0.1, 0.35), (0.3, 0.35), (0.3, 0.2), (0.1, 0.2)],
            'T': [(0.1, 0.5), (0.3, 0.5), (0.2, 0.5), (0.2, 0.2)],
            'U': [(0.1, 0.5), (0.1, 0.3), (0.2, 0.2), (0.3, 0.3), (0.3, 0.5)],
            'V': [(0.1, 0.5), (0.2, 0.2), (0.3, 0.5)],
            'W': [(0.1, 0.5), (0.1, 0.3), (0.2, 0.4), (0.3, 0.3), (0.3, 0.5)],
            'X': [(0.1, 0.5), (0.3, 0.2), (0.2, 0.35), (0.1, 0.2), (0.3, 0.5)],
            'Y': [(0.1, 0.5), (0.2, 0.35), (0.3, 0.5), (0.2, 0.35), (0.2, 0.2)],
            'Z': [(0.1, 0.5), (0.3, 0.5), (0.1, 0.2), (0.3, 0.2)],
        }

        # Encontrar la dimensión horizontal más grande entre todas las letras
        max_width = max(point[0] for points in alphabet_points.values() for point in points)
        letter_spacing = max_width # Agregar un poco más para el espacio entre letras

        # Iterar sobre cada letra del nombre
        for index, letter in enumerate(name.upper()):
            if letter in alphabet_points:
                print(f"Letra '{letter}' definida, escribiendo...")
                points = alphabet_points[letter]
                for (x, y) in points:
                    theta1, theta2 = self.inverse_kinematics(start_x + x, start_y + y)
                    self.move_servos_smoothly(theta1, theta2)
                    time.sleep(0.5)

                # Mover el efector a la siguiente posición horizontal para evitar superposiciones
                if index < len(name) - 1:  # No es necesario mover después de la última letra
                    print("Moviendo al siguiente carácter...")
                    start_x += letter_spacing
                    time.sleep(0.5)  # Espera entre letras

            else:
                # Movimiento por defecto si la letra no está definida
                print(f"Letra '{letter}' no definida, saltando...")
                self.move_servos_smoothly(0, 0)
                time.sleep(0.5)

        # Retornar a la posición inicial al finalizar
        print("Escritura completa. Retornando a posición inicial...")
        self.move_servos_smoothly(0, 0)

    def move_efector_to_next_character(self):
        """
        Mueve el efector final hacia la derecha una cierta distancia para escribir el siguiente carácter.
        """
        # Ajustar las coordenadas para el desplazamiento horizontal entre letras
        x_shift = 0.1  # Desplazamiento horizontal reducido para letras más pequeñas (ajusta según la escala)
        y_current = 0  # Suponiendo que el eje Y se mantiene igual

        # Obtener la posición actual del efector
        try:
            x_current = float(self.lineEdit.text()) if self.lineEdit.text() else 0.0
        except ValueError:
            x_current = 0.0  # En caso de error, se usa un valor predeterminado

        # Nueva posición X para el próximo carácter
        x_new = x_current + x_shift

        # Calcular los ángulos inversos para alcanzar la nueva posición
        theta1, theta2 = self.inverse_kinematics(x_new, y_current)

        # Mover suavemente a la nueva posición
        self.move_servos_smoothly(theta1, theta2)

        # Actualizar la UI con la nueva posición
        self.lineEdit.setText(f"{x_new:.2f}")

    def write_custom_word(self):
        word = self.lineEdit_3.text()
        self.write_name(word)

    def draw_logo(self, logo_name):
        # Lógica para trazar los logos específicos
        self.move_servos_smoothly(0, 0)
        time.sleep(2)  # Espera para que el usuario coloque el papel
        # Implementar lógica para trazar el logo paso a paso
        if logo_name == "Puma":
            # Lógica de trazado para Puma
            pass
        elif logo_name == "Toyota":
            # Lógica de trazado para Toyota
            pass
        elif logo_name == "Apple":
            # Lógica de trazado para Apple
            pass
        elif logo_name == "Pepsi":
            # Lógica de trazado para Pepsi
            pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
