from PyQt5 import QtCore, QtGui, QtWidgets
import math
import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from roboticstoolbox.backends.PyPlot import PyPlot

# Dimensiones del robot (ajustables)
d0 = 0.5  # Longitud del primer eslabón
d1 = 1.0  # Longitud del segundo eslabón
d2 = 0.8  # Longitud del tercer eslabón
d3 = 0.4  # Longitud del cuarto eslabón

class Ui_Dialog(object):
    def __init__(self):
        self.robot = self.create_robot()
        self.simulation = PyPlot()
        self.simulation.launch()
        self.simulation.add(self.robot)

    def create_robot(self):
        R = [
            RevoluteDH(d=d0, alpha=math.pi/2, a=0, offset=0),
            RevoluteDH(d=0, alpha=0, a=d1, offset=math.pi/2),
            RevoluteDH(d=0, alpha=0, a=d2, offset=0),
            RevoluteDH(d=0, alpha=0, a=d3, offset=0)
        ]
        robot = DHRobot(R, name='Bender')
        robot.q = [0, 0, 0, 0]
        return robot

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        
        # Label y LineEdit para el eje X
        self.label_x = QtWidgets.QLabel(Dialog)
        self.label_x.setGeometry(QtCore.QRect(30, 30, 50, 20))
        self.label_x.setText("X:")
        
        self.lineEdit_x = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_x.setGeometry(QtCore.QRect(80, 30, 100, 20))
        
        # Label y LineEdit para el eje Y
        self.label_y = QtWidgets.QLabel(Dialog)
        self.label_y.setGeometry(QtCore.QRect(30, 60, 50, 20))
        self.label_y.setText("Y:")
        
        self.lineEdit_y = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_y.setGeometry(QtCore.QRect(80, 60, 100, 20))
        
        # Label y LineEdit para el eje Z
        self.label_z = QtWidgets.QLabel(Dialog)
        self.label_z.setGeometry(QtCore.QRect(30, 90, 50, 20))
        self.label_z.setText("Z:")
        
        self.lineEdit_z = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_z.setGeometry(QtCore.QRect(80, 90, 100, 20))
        
        # Botón para mover el robot
        self.pushButton_move = QtWidgets.QPushButton(Dialog)
        self.pushButton_move.setGeometry(QtCore.QRect(30, 130, 150, 30))
        self.pushButton_move.setText("Mover a Coordenadas")
        self.pushButton_move.clicked.connect(self.move_to_position)
        
        # Labels para mostrar ángulos calculados
        self.label_theta1 = QtWidgets.QLabel(Dialog)
        self.label_theta1.setGeometry(QtCore.QRect(30, 170, 100, 20))
        self.label_theta1.setText("Theta1: ###")
        
        self.label_theta2 = QtWidgets.QLabel(Dialog)
        self.label_theta2.setGeometry(QtCore.QRect(30, 200, 100, 20))
        self.label_theta2.setText("Theta2: ###")
        
        self.label_theta3 = QtWidgets.QLabel(Dialog)
        self.label_theta3.setGeometry(QtCore.QRect(30, 230, 100, 20))
        self.label_theta3.setText("Theta3: ###")
        
        self.label_theta4 = QtWidgets.QLabel(Dialog)
        self.label_theta4.setGeometry(QtCore.QRect(30, 260, 100, 20))
        self.label_theta4.setText("Theta4: ###")

    def move_to_position(self):
        try:
            # Obtener valores de los campos de texto
            x = float(self.lineEdit_x.text()) if self.lineEdit_x.text() else 0.0
            y = float(self.lineEdit_y.text()) if self.lineEdit_y.text() else 0.0
            z = float(self.lineEdit_z.text()) if self.lineEdit_z.text() else 0.0
            
            # Calcular ángulos inversos (IK)
            theta1, theta2, theta3, theta4 = self.inverse_kinematics(x, y, z)
            
            # Mostrar ángulos en la interfaz
            self.label_theta1.setText(f"Theta1: {theta1:.2f}")
            self.label_theta2.setText(f"Theta2: {theta2:.2f}")
            self.label_theta3.setText(f"Theta3: {theta3:.2f}")
            self.label_theta4.setText(f"Theta4: {theta4:.2f}")
            
            # Asignar ángulos al robot para mover la simulación
            self.robot.q = [np.radians(theta1), np.radians(theta2), np.radians(theta3), np.radians(theta4)]
            self.simulation.step()
            
        except ValueError:
            print("Error: Entrada no válida en los campos de posición.")

    def inverse_kinematics(self, x, y, z):
        global d0, d1, d2, d3
        try:
            # Cálculo de ángulos utilizando el modelo DH
            theta1 = math.atan2(y, x)
            r = math.sqrt(x**2 + y**2)
            s = z - d0
            d = math.sqrt(r**2 + s**2)

            # Ley de cosenos para obtener theta2 y theta3
            cos_theta3 = (d**2 - d1**2 - d2**2) / (2 * d1 * d2)
            theta3 = math.acos(np.clip(cos_theta3, -1, 1))
            theta2 = math.atan2(s, r) - math.atan2(d2 * math.sin(theta3), d1 + d2 * math.cos(theta3))
            theta4 = 0  # Asumimos que theta4 es 0 para mantener el efector alineado

            # Convertir ángulos a grados
            theta1, theta2, theta3, theta4 = map(np.degrees, [theta1, theta2, theta3, theta4])

            # Asegurarse de que los ángulos están en el rango [0, 180]
            theta1 = max(0, min(180, theta1))
            theta2 = max(0, min(180, theta2))
            theta3 = max(0, min(180, theta3))
            theta4 = max(0, min(180, theta4))

            return theta1, theta2, theta3, theta4

        except ValueError:
            print("Error en los cálculos de cinemática inversa: valores fuera de rango.")
            return 0, 0, 0, 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
