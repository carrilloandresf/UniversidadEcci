from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath.base import tr2rpy
import math

# Definir los parámetros de los enlaces
a1 = 12  # Distancia del primer eslabón en el eje Z (altura de la base)
a2 = 14  # Longitud del primer brazo en el eje X (horizontal)
a3 = 6   # Longitud del segundo brazo en el eje X
a4 = 4   # Longitud del eslabón final (muñeca)

# Ángulos iniciales para las articulaciones
q1 = math.pi / 2  # Rotación de la base (90 grados)
q2 = 0            # Primera articulación del brazo
q3 = 0            # Segunda articulación del brazo
q4 = 0            # Muñeca

# Crear las articulaciones rotativas con parámetros DH
R = []
# Articulación 1: Rotación de la base (alrededor del eje Z)
R.append(RevoluteDH(d=a1, alpha=math.pi/2, a=0, offset=0))

# Articulación 2: Primer eslabón horizontal en el brazo
R.append(RevoluteDH(d=0, alpha=0, a=a2, offset=0))

# Articulación 3: Segundo eslabón horizontal en el brazo
R.append(RevoluteDH(d=0, alpha=0, a=a3, offset=0))

# Articulación 4: Eslabón final o muñeca (movimiento de la pinza)
R.append(RevoluteDH(d=0, alpha=0, a=a4, offset=0))

# Definir el robot con las articulaciones creadas
Robot = DHRobot(R, name='Bender')

# Mostrar la estructura del robot
print(Robot)

# Abrir la interfaz de enseñanza interactiva con q1 en 90 grados
Robot.teach([q1, q2, q3, q4], 'rpy/zyx', limits=[-30, 30, -30, 30, -10, 40])

# Cálculo de la matriz de transformación homogénea (MTH) con los ángulos actuales
MTH = Robot.fkine([q1, q2, q3, q4])
print("Matriz de Transformación Homogénea (MTH):")
print(MTH)

# Calcular y mostrar los ángulos Roll, Pitch y Yaw
rpy_angles = tr2rpy(MTH.R, 'deg', 'zyx')
print(f'Roll, Pitch, Yaw = {rpy_angles}')
