import RPi.GPIO as GPIO
from time import sleep, time  # Aquí estamos importando 'time' también

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
        pulse_start = time()  # Aquí usamos 'time()' que ahora está importado
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
        # Imprimir el estado de los sensores
        estado_cny70 = detectar_vaso()
        distancia = medir_distancia()

        print(f"Estado de CNY70 (¿Vaso detectado?): {estado_cny70}")
        print(f"Distancia medida con sensor ultrasónico: {distancia} cm")

        # Lógica del sistema
        if estado_cny70 == 0:  # Si no detecta vaso
            print("Esperando a que el vaso se coloque...")
            mover_motor_paso_a_paso_1(1)  # Mover el motor 1 hasta que se coloque un vaso

        # Si el CNY70 detecta un vaso
        elif estado_cny70 == 1:
            print("Vaso detectado, comenzando llenado...")
            sleep(1)

            # Mover motor 2 (banda) para llenar el vaso
            mover_motor_paso_a_paso_2(10)  # Ajusta según la cantidad de medicación que debe despachar

            # Esperar que el sensor ultrasónico detecte que el vaso está lleno
            while distancia > 5:  # Ajusta el umbral según el tamaño del vaso
                print("Esperando que el vaso se llene...")
                distancia = medir_distancia()
                sleep(0.5)

            # Detener la banda
            print("Vaso lleno, deteniendo la banda.")
            mover_motor_paso_a_paso_2(0)  # Detener el motor de la banda

            # Hacer que el motor 1 gire nuevamente
            print("Moviendo el motor 1 para preparar el siguiente vaso.")
            mover_motor_paso_a_paso_1(1)  # Gira el motor hasta el siguiente vaso

        sleep(1)  # Pausa de 1 segundo entre las iteraciones

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()