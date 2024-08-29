import gpiod
import time

# Definir el chip GPIO, usualmente /dev/gpiochip0
chip = gpiod.Chip('gpiochip0')

# Lista de pines GPIO a utilizar (del 2 al 27)
pins = list(range(2, 28))

# Configurar las líneas GPIO como salidas
lines = chip.get_lines(pins)
lines.request(consumer="led_control", type=gpiod.LINE_REQ_DIR_OUT)

# Encender los LEDs uno por uno con un retardo de 0.5 segundos
try:
    for i in range(len(pins)):
        # Encender el LED correspondiente
        values = [1 if j == i else 0 for j in range(len(pins))]
        lines.set_values(values)
        time.sleep(0.5)  # Esperar 0.5 segundos

        # Apagar el LED correspondiente
        values[i] = 0
        lines.set_values(values)
        time.sleep(0.5)  # Esperar 0.5 segundos

finally:
    # Liberar las líneas GPIO
    lines.release()
