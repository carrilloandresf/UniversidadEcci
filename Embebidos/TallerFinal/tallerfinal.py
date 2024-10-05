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

# Pines del motor paso a paso
MOTOR_PINS = [12, 13, 16, 19]  # Pines conectados al motor
GPIO.setup(MOTOR_PINS, GPIO.OUT)

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

vuelta_actual = 0


# Configuración de pines de entrada y salida
GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)
GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)
GPIO.setup(Buzzer_PIN, GPIO.OUT)  # Configurar Buzzer_PIN como salida

# Configurar los pines del motor paso a paso
for pin in MOTOR_PINS:
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
STEPS_PER_REVOLUTION = 4096 / 8  # Ajusta según tu motor

# Tiempo de delay entre pasos para ajustar velocidad
STEP_DELAY = 0.001  # Ajustado para el motor

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
    GPIO.output(Avance, False)
    GPIO.output(Retroceso, False)

# Función para mover el servomotor a un ángulo dado
def mover_servo(angulo):
    duty_cycle = 2 + (angulo / 18)  # Calcular el ciclo de trabajo
    servo.ChangeDutyCycle(duty_cycle)
    sleep(0.05)  # Pausar brevemente para permitir el movimiento

# Función para activar buzzer por medio segundo
def activar_buzzer(Caracter):
    global flat
    if flat == Caracter:
        return
    GPIO.output(Buzzer_PIN, True)
    sleep(0.5)
    GPIO.output(Buzzer_PIN, False)
    flat = Caracter

# Función para activar el movimiento del motor paso a paso
def mover_motor_paso_a_paso(num_turns):
    global vuelta_actual
    total_steps = int(num_turns * STEPS_PER_REVOLUTION)

    vuelta_actual += 1
    lcd_text(f"Vuelta: {vuelta_actual}", 0x80)

    # Girar el motor por el número de pasos calculado
    for step in range(total_steps):
        for sequence in STEP_SEQUENCE:
            for pin in range(4):
                GPIO.output(MOTOR_PINS[pin], sequence[pin])
            sleep(STEP_DELAY)
        lcd_text(f"Paso: {step}", 0xC0)
    

# Inicializa la pantalla LCD al inicio
lcd_init()

lcd_text("Universidad ECCI", 0x80)
sleep(1)

try:
    while True:
        toggle1 = GPIO.input(TOGGLE_1)  # Lee entrada de avance
        toggle2 = GPIO.input(TOGGLE_2)  # Lee entrada de retroceso

        print(f"TOGGLE_1: {toggle1}, TOGGLE_2: {toggle2}", end='\r')

        # Si ambas entradas están inactivas (falsas), mover el servomotor
        if toggle1 == 0 and toggle2 == 0:
            detener_motor_dc()
            activar_buzzer(0)
            lcd_text("Servo: 0 a 180", 0x80)

            # Recorrer de 0 a 180 grados
            for angulo in range(0, 181, 10):
                mover_servo(angulo)

            # Regresar de 180 a 0 grados
            for angulo in range(180, -1, -10):
                mover_servo(angulo)

        # Si solo TOGGLE_1 está activo (verdadero), activar avance
        elif toggle1 == 1 and toggle2 == 0:
            activar_buzzer(1)
            activar_avance()

        # Si solo TOGGLE_2 está activo (verdadero), activar retroceso
        elif toggle2 == 1 and toggle1 == 0:
            activar_buzzer(2)
            activar_retroceso()

        # Si ambas entradas están activas (verdaderas), ejecutar vueltas del motor paso a paso
        elif toggle1 == 1 and toggle2 == 1:
            detener_motor_dc()
            activar_buzzer(3)

            # Número de vueltas que el motor debe dar (ajústalo según necesites)
            num_turns = 1  # Cambia esto al número de vueltas deseadas

            # Llamar a la función de movimiento del motor paso a paso
            mover_motor_paso_a_paso(num_turns)

        # Pausa breve para evitar lectura continua excesiva
        sleep(0.1)

except KeyboardInterrupt:
    print("Deteniendo programa")
finally:
    # Limpia la configuración de los GPIO al terminar
    GPIO.cleanup()
