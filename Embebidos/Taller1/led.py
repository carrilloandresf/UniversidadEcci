import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# Configurar la numeración de los pines
GPIO.setmode(GPIO.BCM)

# Lista de pines GPIO a utilizar (del 2 al 27)
pins = list(range(2, 28))

# Configurar cada pin como salida
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Encender los LEDs uno por uno con un retardo de 0.5 segundos
try:
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)  # Encender el LED
        time.sleep(0.5)              # Esperar 0.5 segundos
        GPIO.output(pin, GPIO.LOW)  # Encender el LED
        time.sleep(0.5)              # Esperar 0.5 segundos

finally:
    # Limpiar la configuración de los pines
    GPIO.cleanup()
