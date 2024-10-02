import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definición de pines
TOGGLE_1 = 4
TOGGLE_2 = 6
LCD_RS = 10
LCD_E = 9
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25
Avance = 17
Retroceso = 18

# Pines del motor paso a paso (nuevo)
BitMot0 = 12
BitMot1 = 13
BitMot2 = 16
BitMot3 = 19

motor_pins = [BitMot0, BitMot1, BitMot2, BitMot3]

# Pin para el buzzer
BUZZER = 21

# Pines del servomotor (puente H)
Servo_PWM = 18  # Pin de señal PWM del servomotor

# Configuración de pines (solo una vez)
GPIO.setup(TOGGLE_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TOGGLE_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Configuración del servomotor
GPIO.setup(Servo_PWM, GPIO.OUT)
servo = GPIO.PWM(Servo_PWM, 50)  # PWM a 50Hz
servo.start(0)

# Configuración del buzzer
def buzzer_sound(duration=0.1):
    GPIO.output(BUZZER, True)
    sleep(duration)
    GPIO.output(BUZZER, False)

# Secuencia de pasos del motor paso a paso
step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

def set_step(step):
    for pin in range(4):
        GPIO.output(motor_pins[pin], step[pin])

def rotate_motor(steps, delay=0.01):
    for _ in range(steps):
        for step in step_sequence:
            set_step(step)
            sleep(delay)

def return_to_initial_position(steps, delay=0.01):
    for _ in range(steps):
        for step in reversed(step_sequence):
            set_step(step)
            sleep(delay)

def lcd_write(bits, mode):
    try:
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
    except Exception as e:
        print(f"Error al escribir en la LCD: {e}")

def lcd_toggle_enable():
    sleep(0.0005)
    GPIO.output(LCD_E, True)
    sleep(0.0005)
    GPIO.output(LCD_E, False)
    sleep(0.0005)

def lcd_init():
    lcd_write(0x33, GPIO.LOW)
    lcd_write(0x32, GPIO.LOW)
    lcd_write(0x06, GPIO.LOW)
    lcd_write(0x0C, GPIO.LOW)
    lcd_write(0x28, GPIO.LOW)
    lcd_write(0x01, GPIO.LOW)
    sleep(0.0005)

def lcd_texto(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, GPIO.LOW)
    for i in range(16):
        lcd_write(ord(message[i]), GPIO.HIGH)

def LCD(message):
    lcd_init()
    lcd_texto(message, 0x80)
    sleep(0.01)

def Movimiento(AR):
    if AR == 1:
        GPIO.output(Avance, True)
        GPIO.output(Retroceso, False)
    elif AR == 0:
        GPIO.output(Avance, False)
        GPIO.output(Retroceso, True)
    else:
        GPIO.output(Avance, False)
        GPIO.output(Retroceso, False)

def mover_servo(angulo):
    duty_cycle = angulo / 18 + 2
    servo.ChangeDutyCycle(duty_cycle)

try:
    estado_anterior = None

    while True:
        toggle1 = GPIO.input(TOGGLE_1)
        toggle2 = GPIO.input(TOGGLE_2)

        # Estado actual para comparar cambios
        estado_actual = (toggle1, toggle2)

        # Si se detecta un cambio de estado, activar el buzzer
        if estado_actual != estado_anterior:
            buzzer_sound()
            estado_anterior = estado_actual

        # Si ambas entradas están inactivas
        if toggle1 == 0 and toggle2 == 0:
            LCD("Servomotor 180\u00b0")  # Usar código Unicode para el símbolo de grado
            mover_servo(180)
            sleep(1)  # Esperar un segundo
            mover_servo(0)  # Regresar a la posición cero
        # Si solo TOGGLE_1 está activo
        elif toggle1 == 1 and toggle2 == 0:
            LCD("Giro derecha")
            Movimiento(1)
        # Si solo TOGGLE_2 está activo
        elif toggle2 == 1 and toggle1 == 0:
            LCD("Giro izquierda")
            Movimiento(0)
        # Si ambos están activos
        elif toggle1 == 1 and toggle2 == 1:
            LCD("Motor paso")
            rotate_motor(2048)  # Rotar el motor paso a paso
        else:
            Movimiento(-1)  # Detener el motor DC si no hay condiciones activas
        
        sleep(0.5)

except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()