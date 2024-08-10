"""
Es un LED que se enciende y se apaga con un tiempo de espera de 0.5 segundos.
Para encender el LED se debe encender el GPIO 17.
Para apagar el LED se debe apagar el GPIO 17.
"""

from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(3)
    led.off()
    sleep(3)