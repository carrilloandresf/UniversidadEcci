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

BitMot0 = 32
BitMot1 = 33
BitMot2 = 36
BitMot3 = 35

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

# Configuración de pines (solo una vez)
GPIO.setup(TOGGLE_1, GPIO.IN)
GPIO.setup(TOGGLE_2, GPIO.IN)

for salida in bits_datos:
    GPIO.setup(salida, GPIO.OUT)
    
GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)

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
        elif GPIO.input(TOGGLE_1) == 1 and GPIO.input(TOGGLE_2) == 1:  # Si ambos están activado
            LCD("Motor paso")
            
        else:
            LCD("Detenido | ECCI")
            Movimiento(-1)  # Asegurarse de detener el movimiento si no hay entradas activadas
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()  # Asegura la limpieza adecuada de los pines
