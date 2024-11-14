from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np

# Definición del robot usando parámetros DH aproximados
# (ajusta los valores según las dimensiones de tu diseño)

robot = DHRobot([
    RevoluteDH(d=0.1, a=0, alpha=np.pi/2),    # Primer eslabón
    RevoluteDH(d=0, a=0.3, alpha=0),           # Segundo eslabón
    RevoluteDH(d=0, a=0.3, alpha=0),           # Tercer eslabón
    RevoluteDH(d=0.1, a=0, alpha=np.pi/2),     # Cuarto eslabón (muñeca rotatoria)
    RevoluteDH(d=0.1, a=0, alpha=0)            # Eslabón final (para la pinza)
], name="BrazoRobotico")

# Visualización de las configuraciones iniciales
print(robot)

# Simulación en posición inicial
q0 = [0, 0, 0, 0, 0]  # Ajusta los ángulos iniciales
robot.plot(q0)