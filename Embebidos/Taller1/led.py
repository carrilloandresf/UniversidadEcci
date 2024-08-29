import gpiod
import time

# Seleccionar el chip GPIO, usualmente /dev/gpiochip0
chip = gpiod.Chip('gpiochip0')

# Seleccionar la línea GPIO (por ejemplo, GPIO 17)
line = chip.get_line(17)

# Configurar la línea como salida
config = gpiod.LineRequest()
config.consumer = "blink"
config.request_type = gpiod.LineRequest.DIRECTION_OUTPUT

line.request(config)

# Controlar el LED encendiéndolo y apagándolo
try:
    while True:
        line.set_value(1)  # Encender
        time.sleep(1)
        line.set_value(0)  # Apagar
        time.sleep(1)
finally:
    line.release()
