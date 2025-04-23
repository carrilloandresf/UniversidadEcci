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

STEP_DELAY = 0.001  # Ajustado para el motor

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
def mover_motor_paso_a_paso_2():
    for sequence in STEP_SEQUENCE:
        for pin in range(4):
            GPIO.output(MOTOR_PINS_2[pin], sequence[pin])
        sleep(STEP_DELAY)

# Función para revisar si el sensor CNY70 detecta un vaso (con lógica inversa)
def detectar_vaso():
    return GPIO.input(CNY70_PIN) == 0  # El CNY70 devuelve 0 cuando detecta un vaso

# Inicializa los pines
try:
    while True:
        # Leer el estado del sensor CNY70
        estado_cny70 = detectar_vaso()
        print(f"Estado de CNY70 (¿Vaso detectado?): {'Sí' if estado_cny70 else 'No'}")

        # Lógica del sistema
        if not estado_cny70:  # Si el CNY70 no detecta vaso (el valor es 1)
            print("Esperando a que el vaso se coloque...")
            mover_motor_paso_a_paso_1(10)  # Mueve el motor 1 hasta que se coloque un vaso

        # Si el CNY70 detecta un vaso (el valor es 0)
        elif estado_cny70:
            print("Vaso detectado, comenzando llenado...")
            sleep(0.2)  # Esperar un poco para estabilizar el proceso

            # Mover motor 2 (banda) para llenar el vaso
            print("Iniciando el llenado...")
            mover_motor_paso_a_paso_2()  # Mantiene el motor girando indefinidamente

            # Esperar que el sensor ultrasónico detecte que el vaso está lleno
            distancia = medir_distancia()
            while distancia > 5:  # Ajusta el umbral según el tamaño del vaso
                print("Esperando que el vaso se llene...")
                distancia = medir_distancia()  # Medir nuevamente la distancia
                sleep(0.5)  # Pausa para medir la distancia periódicamente

            # Detener la banda cuando el vaso esté lleno
            print("Vaso lleno, deteniendo la banda.")
            GPIO.output(MOTOR_PINS_2[0], GPIO.LOW)
            GPIO.output(MOTOR_PINS_2[1], GPIO.LOW)
            GPIO.output(MOTOR_PINS_2[2], GPIO.LOW)
            GPIO.output(MOTOR_PINS_2[3], GPIO.LOW)

            # Hacer que el motor 1 gire nuevamente
            print("Moviendo el motor 1 para preparar el siguiente vaso.")
            mover_motor_paso_a_paso_1(30)  # Gira el motor hasta el siguiente vaso

        sleep(1)  # Pausa de 1 segundo entre las iteraciones

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()