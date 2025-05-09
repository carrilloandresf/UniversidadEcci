import RPi.GPIO as GPIO
from time import sleep, time

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines del motor paso a paso 1 (motor de los vasos)
MOTOR_PINS_1 = [12, 13, 16, 19]

# Pines del motor paso a paso 2 (motor de la banda para despachar medicamentos)
MOTOR_PINS_2 = [27, 26, 22, 17]

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

# Secuencia de pasos medio paso (Half-Step)
STEP_SEQUENCE_FULL = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

# Número de pasos por revolución para el motor paso a paso
STEPS_PER_REVOLUTION = 4096 / 8  # Ajusta según tu motor

STEP_DELAY = 0.005  # Ajustado para el motor (más lento para suavizar el movimiento)
STEP_DELAY2 = 0.03

FLAT = 0

def imprimir_sobre_linea(texto):
    print(f"\r{texto}", end='', flush=True)

# Función para medir la distancia con el sensor ultrasónico
def medir_distancia(intentos=7):
    distancias = []
    for _ in range(intentos):
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
        distancias.append(distance)
        sleep(0.2)  # Pausa para evitar lecturas consecutivas rápidas que puedan interferir
    
    # Promediar las distancias medidas
    distancia_promediada = sum(distancias) / len(distancias)
    imprimir_sobre_linea(f"                                      Distancia promedio: {distancia_promediada:.2f} cm   ")
    return distancia_promediada

# Función para mover el motor paso a paso 1 (motor de los vasos) de manera suave
def mover_motor_paso_a_paso_1(steps):
    for step in range(steps):
        for sequence in STEP_SEQUENCE_FULL:
            for pin in range(4):
                GPIO.output(MOTOR_PINS_1[pin], sequence[pin])
            sleep(STEP_DELAY)

# Función para mover el motor paso a paso 2 (motor de la banda de medicamentos) de manera suave
def mover_motor_paso_a_paso_2(steps):
    for step in range(steps):
        for sequence in STEP_SEQUENCE_FULL:
            for pin in range(4):
                GPIO.output(MOTOR_PINS_2[pin], sequence[pin])
            sleep(STEP_DELAY)

# Función para revisar si el sensor CNY70 detecta un vaso (con lógica inversa)
def detectar_vaso():
    return GPIO.input(CNY70_PIN) == 0  # El CNY70 devuelve 0 cuando detecta un vaso

# Función para detener el motor de la banda (motor 2)
def detener_motor_banda():
    for pin in MOTOR_PINS_2:
        GPIO.output(pin, GPIO.LOW)

# Inicializa los pines
try:
    while True:
        # Leer el estado del sensor CNY70
        estado_cny70 = detectar_vaso()

        # Lógica del sistema
        if not estado_cny70:  # Si el CNY70 no detecta vaso (el valor es 1)
            FLAT = 0
            imprimir_sobre_linea("Esperando a que el vaso se coloque...                            ")
            mover_motor_paso_a_paso_1(10)  # Mueve el motor 1 hasta que se coloque un vaso

        # Si el CNY70 detecta un vaso (el valor es 0)
        elif estado_cny70:
            if FLAT == 0:
                mover_motor_paso_a_paso_1(4)
                FLAT = 1
            # Mover motor 2 (banda) para llenar el vaso
            imprimir_sobre_linea("Llenando...        ")

            # Esperar que el sensor ultrasónico detecte que el vaso está lleno
            distancia = medir_distancia()
            if distancia <= 7.5:
                imprimir_sobre_linea(f"Acomodando vaso... distancia detectada {distancia:.2f}   cm                  ")
                sleep(2.5)
                mover_motor_paso_a_paso_1(100)
                continue  

            mover_motor_paso_a_paso_2(30)  # Mantiene el motor girando indefinidamente

        sleep(0.01)  # Pausa más corta para mayor fluidez y control de la ejecución

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    GPIO.cleanup()