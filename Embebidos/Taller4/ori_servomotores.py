import RPi.GPIO as GPIO
from time import sleep

# Configuración inicial de los pines GPIO
GPIO.setmode(GPIO.BCM)  # Cambié GPIOBCM por GPIO.BCM
GPIO.setwarnings(False)

# Configuración del pin y la frecuencia del PWM
pwmgpio13 = 13
frecuencia = 50
GPIO.setup(pwmgpio13, GPIO.OUT)
pwm = GPIO.PWM(pwmgpio13, frecuencia)

# Función para calcular el duty cycle en función del ángulo
def porcentaje(angulo):
    if angulo > 180 or angulo < 0:
        return False

    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    return comienzo + (radio * angulo)

try:
    while True:  # Bucle infinito
        # Iniciar el PWM para que el motor esté a 0°
        pwm.start(porcentaje(0))
        sleep(1)  # Esperar 1 segundo

        # Cambiar el ciclo de trabajo a 180°
        pwm.ChangeDutyCycle(porcentaje(180))
        sleep(1)  # Esperar 1 segundo

        # Cambiar el ciclo de trabajo a 90°
        pwm.ChangeDutyCycle(porcentaje(90))
        sleep(1)  # Esperar 1 segundo
        
        # Parar el PWM
        pwm.stop()

except KeyboardInterrupt:  # Manejo de la interrupción del teclado
    pass

finally:
    GPIO.cleanup()  # Limpieza de la configuración de los pines GPIO