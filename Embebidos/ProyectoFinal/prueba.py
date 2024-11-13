import RPi.GPIO as GPIO
import time

# Pines del motor paso a paso
BitMot0 = 12
BitMot1 = 13
BitMot2 = 16
BitMot3 = 19
motor_pins = [BitMot0, BitMot1, BitMot2, BitMot3]

# Secuencia de pasos para el motor 28BYJ-48
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Configurar los pines de salida
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def move_forward(steps, delay):
    for _ in range(steps):
        for step in step_sequence:
            for pin in range(4):
                GPIO.output(motor_pins[pin], step[pin])
            time.sleep(delay)

try:
    # Mover el motor hacia adelante con una demora de 0.002 segundos por paso
    move_forward(steps=512, delay=0.002)
finally:
    # Limpiar la configuración de GPIO al finalizar
    GPIO.cleanup()
