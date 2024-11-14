from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath.base import tr2rpy
import math

# Definir los parámetros de los enlaces
a1 = 12
a2 = 14
a3 = 6
a4 = 4

# Ángulos iniciales
q1 = 0
q2 = 0

# Crear las articulaciones rotativas con parámetros DH
R = []
R.append(RevoluteDH(d=a1, alpha=math.pi/2, a=a2, offset=0))
R.append(RevoluteDH(d=a3, alpha=0, a=a4, offset=0))

# Definir el robot con las articulaciones creadas
Robot = DHRobot(R, name='Bender')

# Mostrar la estructura del robot
print(Robot)

# Abrir la interfaz de enseñanza interactiva
Robot.teach([q1, q2], 'rpy/zyx', limits=[[-30, 30], [-30, 30]])

# Cálculo de la matriz de transformación homogénea (MTH) con los ángulos actuales
MTH = Robot.fkine([q1, q2])
print("Matriz de Transformación Homogénea (MTH):")
print(MTH)

# Calcular y mostrar los ángulos Roll, Pitch y Yaw
rpy_angles = tr2rpy(MTH.R, 'deg', 'zyx')
print(f'Roll, Pitch, Yaw = {rpy_angles}')
