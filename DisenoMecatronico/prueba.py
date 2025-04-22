import RPi.GPIO as GPIO
from time import sleep, time

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines del motor paso a paso 1 (motor de los vasos)
MOTOR_PINS_1 = [12, 13, 16, 19]

# Pines del motor paso a paso 2 (motor de la banda para despachar medicamentos)
MOTOR_PINS_2 = [17, 22, 26, 27]

# Pines de los sensores
CNY70_PIN = 21  # Sensor CNY70 para detectar el vaso
ULTRASONIDO_TRIG = 23
ULTRASONIDO_ECHO = 24

# Configuración de pines de entrada y salida
GPIO.setup(CNY70_PIN, GPIO.IN)  # Sensor CNY70 como entrada

# Configuración de los motores paso a paso
for pin in MOTOR_PINS_1 + MOTOR_PINS_2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Configuración de los pines del sensor ultrasónico
GPIO.setup(ULTRASONIDO_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIDO_ECHO, GPIO.IN)

# Secuencia de pasos para los motores paso a paso (ULN2003AN)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Número de pasos por revolución para el motor paso a paso
STEPS_PER_REVOLUTION = 4096 / 8  # Ajusta según tu motor
STEP_DELAY = 0.01  # Ajustado para el motor

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

# Función para mover el motor paso a paso 1 (motor de los vasos)
def mover_motor_paso_a_paso_1(steps):
    for step in range(steps):
        for sequence in STEP_SEQUENCE:
            for pin in range(4):
                GPIO.output(MOTOR_PINS_1[pin], sequence[pin])
            sleep(STEP_DELAY)

# Función para mover el motor paso a paso 2 (motor de la banda de medicamentos)
def mover_motor_paso_a_paso_2(steps):
    for step in range(steps):
        for sequence in STEP_SEQUENCE:
            for pin in range(4):
                GPIO.output(MOTOR_PINS_2[pin], sequence[pin])
            sleep(STEP_DELAY)

# Función para revisar si el sensor CNY70 detecta un vaso
def detectar_vaso():
    return GPIO.input(CNY70_PIN)

# Inicializa los pines
try:
    while True:
        # Leer el estado del sensor CNY70
        estado_cny70 = detectar_vaso()
        print(f"Estado de CNY70 (¿Vaso detectado?): {'Sí' if estado_cny70 else 'No'}")

        # Medir la distancia con el sensor ultrasónico
        distancia = medir_distancia()
        print(f"Distancia medida con sensor ultrasónico: {distancia} cm")

        # Mover ambos motores indefinidamente
        print("Moviendo ambos motores indefinidamente...")
        mover_motor_paso_a_paso_1(10)  # Mueve el motor 1 indefinidamente (ajusta el número de pasos)
        mover_motor_paso_a_paso_2(10)  # Mueve el motor 2 indefinidamente (ajusta el número de pasos)
        
        sleep(1)  # Pausa de 1 segundo para ver los resultados

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()