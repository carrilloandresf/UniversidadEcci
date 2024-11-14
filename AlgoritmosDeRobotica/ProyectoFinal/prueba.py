from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Definir el robot utilizando parámetros DH aproximados
robot = DHRobot([
    RevoluteDH(d=0.1, a=0, alpha=np.pi/2),
    RevoluteDH(d=0, a=0.3, alpha=0),
    RevoluteDH(d=0, a=0.3, alpha=0),
    RevoluteDH(d=0.1, a=0, alpha=np.pi/2),
    RevoluteDH(d=0.1, a=0, alpha=0)
], name="BrazoRobotico")

# Posiciones iniciales de las articulaciones
q_initial = [0, 0, 0, 0, 0]

# Crear una figura y un eje para la visualización
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.4)

# Dibujar la posición inicial del robot
plot = robot.plot(q_initial, ax=ax, block=False)

# Crear sliders para cada articulación
sliders = []
slider_axes = []

for i in range(5):
    # Crear un eje para el slider
    ax_slider = plt.axes([0.1, 0.3 - i * 0.05, 0.8, 0.03])
    slider = Slider(ax_slider, f'Articulación {i+1}', -np.pi, np.pi, valinit=0)
    sliders.append(slider)

# Función de actualización cuando se mueve un slider
def update(val):
    # Obtener los valores de los sliders y actualizar la posición del robot
    q = [slider.val for slider in sliders]
    robot.plot(q, ax=ax, block=False)

# Conectar los sliders con la función de actualización
for slider in sliders:
    slider.on_changed(update)

# Mostrar la interfaz interactiva
plt.show()