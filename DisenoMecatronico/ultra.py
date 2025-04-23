import RPi.GPIO as GPIO
from time import sleep, time

# Pines del sensor ultrasónico
ULTRASONIDO_TRIG = 23
ULTRASONIDO_ECHO = 24

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configuración de los pines del sensor ultrasónico
GPIO.setup(ULTRASONIDO_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIDO_ECHO, GPIO.IN)

# Función para medir la distancia con el sensor ultrasónico
def medir_distancia():
    # Enviar pulso de activación
    GPIO.output(ULTRASONIDO_TRIG, True)
    sleep(0.00001)
    GPIO.output(ULTRASONIDO_TRIG, False)
    
    # Medir tiempo del pulso
    while GPIO.input(ULTRASONIDO_ECHO) == 0:
        pulse_start = time()  # Usamos 'time()' que está importado
    while GPIO.input(ULTRASONIDO_ECHO) == 1:
        pulse_end = time()  # También usamos 'time()' aquí
    
    # Calcular la distancia
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Calcular en cm
    return distance

# Ejemplo de uso: medir la distancia
try:
    while True:
        distancia = medir_distancia()
        print(f"Distancia medida con sensor ultrasónico: {distancia} cm")
        sleep(1)  # Pausa de 1 segundo entre mediciones

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()