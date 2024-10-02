import RPi.GPIO as GPIO
from time import sleep

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definición de pines
TOGGLE_1 = 4  # Avance
TOGGLE_2 = 6  # Retroceso
Avance = 17
Retroceso = 18

# Pines del motor paso a paso (nuevo)
BitMot0 = 12
BitMot1 = 13
BitMot2 = 16
BitMot3 = 19
motor_pins = [BitMot0, BitMot1, BitMot2, BitMot3]

# Pines de la LCD
LCD_RS = 10
LCD_E = 9
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

# Pin del servomotor
SERVO_PIN = 20

# Buzzer de cambios
Buzzer_PIN = 21

# Variable de seguimiento de secuencia
flat = 0

# Configuración de pines de entrada y salida
GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)
GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)
GPIO.setup(Buzzer_PIN, GPIO.OUT)  # Configurar Buzzer_PIN como salida

# Configurar los pines del motor paso a paso
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Configuración de pines de la pantalla LCD
lcd_pins = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]
for pin in lcd_pins:
    GPIO.setup(pin, GPIO.OUT)

# Configuración del servomotor
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz para el servomotor
servo.start(0)

# Secuencia de pasos del motor paso a paso (ULN2003AN)
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
STEPS_PER_REVOLUTION = 4096  # Ajusta según tu motor

# Función para inicializar la pantalla LCD
def lcd_init():
    lcd_write(0x33, GPIO.LOW)
    lcd_write(0x32, GPIO.LOW)
    lcd_write(0x06, GPIO.LOW)
    lcd_write(0x0C, GPIO.LOW)
    lcd_write(0x28, GPIO.LOW)
    lcd_write(0x01, GPIO.LOW)
    sleep(0.0005)

def lcd_write(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_D4, bits & 0x10 == 0x10)
    GPIO.output(LCD_D5, bits & 0x20 == 0x20)
    GPIO.output(LCD_D6, bits & 0x40 == 0x40)
    GPIO.output(LCD_D7, bits & 0x80 == 0x80)
    lcd_toggle_enable()
    GPIO.output(LCD_D4, bits & 0x01 == 0x01)
    GPIO.output(LCD_D5, bits & 0x02 == 0x02)
    GPIO.output(LCD_D6, bits & 0x04 == 0x04)
    GPIO.output(LCD_D7, bits & 0x08 == 0x08)
    lcd_toggle_enable()

def lcd_toggle_enable():
    sleep(0.0005)
    GPIO.output(LCD_E, True)
    sleep(0.0005)
    GPIO.output(LCD_E, False)
    sleep(0.0005)

def lcd_text(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, GPIO.LOW)
    for char in message:
        lcd_write(ord(char), GPIO.HIGH)

# Función para activar avance del motor DC
def activar_avance():
    lcd_text("Giro: Avance", 0x80)
    GPIO.output(Avance, True)
    GPIO.output(Retroceso, False)

# Función para activar retroceso del motor DC
def activar_retroceso():
    lcd_text("Giro: Retroceso", 0x80)
    GPIO.output(Avance, False)
    GPIO.output(Retroceso, True)

# Función para detener el motor DC
def detener_motor_dc():
    lcd_text("Motor DC Detenido", 0x80)
    GPIO.output(Avance, False)
    GPIO.output(Retroceso, False)

# Función para mover el servomotor a una posición
def mover_servo(angulo):
    duty_cycle = 2 + (angulo / 18)  # Calcular el ciclo de trabajo
    servo.ChangeDutyCycle(duty_cycle)

# Función para activar buzzer por medio segundo
def activar_buzzer(Caracter):
    global flat
    if flat == Caracter:
        return
    GPIO.output(Buzzer_PIN, True)
    sleep(0.5)
    GPIO.output(Buzzer_PIN, False)
    flat = Caracter

# Inicializa la pantalla LCD al inicio
lcd_init()

# Índice de secuencia del motor paso a paso
step_index = 0
step_count = 0

lcd_text("Universidad ECCI", 0x80)
sleep(1)

try:
    while True:
        toggle1 = GPIO.input(TOGGLE_1)  # Lee entrada de avance
        toggle2 = GPIO.input(TOGGLE_2)  # Lee entrada de retroceso

        print(f"TOGGLE_1: {toggle1}, TOGGLE_2: {toggle2}")

        # Si ambas entradas están inactivas (falsas), mover el servomotor
        if toggle1 == 0 and toggle2 == 0:
            activar_buzzer(0)
            lcd_text("Servo: 90 grados", 0x80)
            mover_servo(90)
            sleep(1)
            mover_servo(0)  # Regresar a la posición inicial

        # Si solo TOGGLE_1 está activo (verdadero), activar avance
        elif toggle1 == 1 and toggle2 == 0:
            activar_buzzer(1)
            activar_avance()

        # Si solo TOGGLE_2 está activo (verdadero), activar retroceso
        elif toggle2 == 1 and toggle1 == 0:
            activar_buzzer(2)
            activar_retroceso()

        # Si ambas entradas están activas (verdaderas), ejecutar un solo paso
        elif toggle1 == 1 and toggle2 == 1:
            activar_buzzer(3)
            # Ejecutar un paso del motor paso a paso
            sequence = STEP_SEQUENCE[step_index]
            for pin in range(4):
                GPIO.output(motor_pins[pin], sequence[pin])
            
            # Actualizar el paso en la LCD
            step_count += 1
            lcd_text(f"Paso: {step_count}", 0x80)

            # Avanzar al siguiente paso en la secuencia
            step_index = (step_index + 1) % len(STEP_SEQUENCE)

            # Pausar brevemente para permitir el movimiento del motor
            sleep(0.01)

        # Pausa breve para evitar lectura continua excesiva
        sleep(0.1)

except KeyboardInterrupt:
    print("Deteniendo programa")
    detener_motor_dc()
    servo.stop()
    GPIO.cleanup()
