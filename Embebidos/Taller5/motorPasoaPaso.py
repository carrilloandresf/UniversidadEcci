import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Definición de pines
TOGGLE_1 = 29
TOGGLE_2 = 31
LCD_RS = 19
LCD_E = 21
LCD_D4 = 15
LCD_D5 = 16
LCD_D6 = 18
LCD_D7 = 22
Avance = 11
Retroceso = 12

# Pines del motor paso a paso
BitMot0 = 32
BitMot1 = 33
BitMot2 = 36
BitMot3 = 35

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]
motor_pins = [BitMot0, BitMot1, BitMot2, BitMot3]

# Configuración de pines (solo una vez)
GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)

for salida in bits_datos:
    GPIO.setup(salida, GPIO.OUT)
    
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)

# Variables de control de movimiento
grados_a_girar = 135  # Ángulo deseado en grados
pasos_por_revolucion = 2048  # Pasos por revolución del motor
pasos = int(pasos_por_revolucion * (grados_a_girar / 360))  # Cálculo de pasos para el ángulo

# Secuencia de pasos del motor
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

def LCD(hora):
    lcd_init()
    lcd_texto(hora, 0x80)
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

try:
    while True:
        if GPIO.input(TOGGLE_1) == 1 and GPIO.input(TOGGLE_2) == 0:  # Si TOGGLE_1 está activado
            LCD("Giro izquierda")
            Movimiento(1)
        elif GPIO.input(TOGGLE_2) == 1 and GPIO.input(TOGGLE_1) == 0:  # Si TOGGLE_2 está activado
            LCD("Giro derecha")
            Movimiento(0)
        elif GPIO.input(TOGGLE_1) == 0 and GPIO.input(TOGGLE_2) == 0:  # Si ambos están activados
            LCD("Motor paso")
            rotate_motor(pasos)  # Rotar el motor a la posición deseada
            sleep(1)  # Esperar un segundo
            #return_to_initial_position(pasos)  # Retornar a la posición inicial
            
        else:
            LCD("Detenido | ECCI")
            Movimiento(-1)  # Asegurarse de detener el movimiento si no hay entradas activadas
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()  # Asegura la limpieza adecuada de los pines
