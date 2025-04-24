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
CNY70_PIN = 21
ULTRASONIDO_TRIG = 23
ULTRASONIDO_ECHO = 24

# Configuración de pines
GPIO.setup(CNY70_PIN, GPIO.IN)
for pin in MOTOR_PINS_1 + MOTOR_PINS_2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
GPIO.setup(ULTRASONIDO_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIDO_ECHO, GPIO.IN)

# Secuencia del motor paso a paso
STEP_SEQUENCE_FULL = [
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

STEP_DELAY = 0.01

def mover_motor(pins):
    for sequence in STEP_SEQUENCE_FULL:
        for i in range(4):
            GPIO.output(pins[i], sequence[i])
        sleep(STEP_DELAY)

def detectar_vaso():
    return GPIO.input(CNY70_PIN) == 0 

def medir_distancia():
    GPIO.output(ULTRASONIDO_TRIG, True)
    sleep(0.00001)
    GPIO.output(ULTRASONIDO_TRIG, False)

    pulse_start = time()
    while GPIO.input(ULTRASONIDO_ECHO) == 0:
        pulse_start = time()
    while GPIO.input(ULTRASONIDO_ECHO) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    return pulse_duration * 17150

def imprimir_sobre_linea(texto):
    print(f"\r{texto}", end='', flush=True)

def mostrar_menu():
    print("\n¿Qué deseas probar?")
    print("1. Motor 1 (vasos)")
    print("2. Motor 2 (banda medicamentos)")
    print("3. Sensor CNY70 (detección de vaso)")
    print("4. Sensor ultrasónico (distancia)")
    return input("Ingresa tu opción (1-4): ")

try:
    opcion = mostrar_menu()
    print("Presiona Ctrl+C para salir.\n")
    
    if opcion == '1':
        while True:
            mover_motor(MOTOR_PINS_1)
            imprimir_sobre_linea("Moviendo motor 1 (vasos)...")

    elif opcion == '2':
        while True:
            mover_motor(MOTOR_PINS_2)
            imprimir_sobre_linea("Moviendo motor 2 (banda medicamentos)...")

    elif opcion == '3':
        while True:
            estado = detectar_vaso()
            imprimir_sobre_linea(f"Sensor CNY70 detecta vaso: {'Sí' if estado else 'No'}     ")
            sleep(0.2)

    elif opcion == '4':
        while True:
            distancia = medir_distancia()
            imprimir_sobre_linea(f"Distancia medida: {distancia:.2f} cm     ")
            sleep(0.3)

    else:
        print("Opción inválida. Reinicia el programa.")

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    GPIO.cleanup()