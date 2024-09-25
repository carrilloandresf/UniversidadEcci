import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#FLAT
FLAT1 = 0
FLAT2 = 0

# Definición de pines
# Pines para los servos
SERVO_1 = 13
SERVO_2 = 16
'''
# Pines para los pulsadores de cada servo
BUTTON_1_POS = 4  # Pulsador para +90 grados del Servo 1
BUTTON_1_NEG = 7  # Pulsador para -90 grados del Servo 1
BUTTON_2_POS = 19  # Pulsador para +90 grados del Servo 2
BUTTON_2_NEG = 27  # Pulsador para -90 grados del Servo 2
'''

PULSE_1 = 4  # Pulsador para +90 grados del Servo 1
PULSE_2 = 7  # Pulsador para +90 grados del Servo 2

# Pines para el LCD
LCD_RS = 10
LCD_E = 9
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

# Configuración de los pines GPIO
GPIO.setup(SERVO_1, GPIO.OUT)
GPIO.setup(SERVO_2, GPIO.OUT)
GPIO.setup(PULSE_1, GPIO.IN)
GPIO.setup(PULSE_2, GPIO.IN)

# Asegúrate de que los pines del LCD estén configurados como salidas
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

# Configuración del PWM para los servos
pwm_servo_1 = GPIO.PWM(SERVO_1, 50)
pwm_servo_2 = GPIO.PWM(SERVO_2, 50)
pwm_servo_1.start(7.5)  # Posición inicial en el centro (0 grados)
pwm_servo_2.start(7.5)  # Posición inicial en el centro (0 grados)

# Función para calcular el duty cycle en función del ángulo
def porcentaje(angulo):
    comienzo = 2.5  # Valor de PWM para -90 grados
    final = 12.5  # Valor de PWM para +90 grados
    radio = (final - comienzo) / 180
    return comienzo + (radio * (angulo + 90))

# Función para escribir en el LCD
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

def LCD(message1, message2):
    lcd_init()
    lcd_texto(message1, 0x80)  # Primera línea
    lcd_texto(message2, 0xC0)  # Segunda línea
    sleep(0.01)

# Función para mover el servo
def mover_servo(pwm_servo, angulo):
    pwm_servo.ChangeDutyCycle(porcentaje(angulo))
    sleep(0.5)

try:
    # Estado inicial
    estado_servo_1 = "Stop"
    estado_servo_2 = "Stop"
    
    while True:
        # Control para el Servo 1
        if GPIO.input(PULSE_1) == GPIO.LOW:
            estado_servo_1 = "Servo_1 giro 90 grados"
            mover_servo(pwm_servo_1, 90)
            FLAT1 = 1
        elif GPIO.input(PULSE_1) == GPIO.HIGH and FLAT1 == 1:
            estado_servo_1 = "Servo_1 giro -90 grados"
            mover_servo(pwm_servo_1, -90)
            FLAT1 = 0
        else:
            estado_servo_1 = "Servo_1 Stop"

        # Control para el Servo 2
        if GPIO.input(PULSE_2) == GPIO.LOW:
            estado_servo_2 = "Servo_2 giro 90 grados"
            mover_servo(pwm_servo_2, 90)
            FLAT2 = 1
        elif GPIO.input(PULSE_2) == GPIO.HIGH and FLAT2 == 1:
            estado_servo_2 = "Servo_2 giro -90 grados"
            mover_servo(pwm_servo_2, -90)
            FLAT2 = 0
        else:
            estado_servo_2 = "Servo_2 Stop"

        # Mostrar en el LCD
        LCD(estado_servo_1, estado_servo_2)
        sleep(0.5)  # Pequeña pausa antes de la siguiente actualización

except KeyboardInterrupt:
    # Limpieza de los GPIO y parada de los PWM
    pwm_servo_1.stop()
    pwm_servo_2.stop()
    GPIO.cleanup()