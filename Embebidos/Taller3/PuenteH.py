import gpiod
from time import sleep
import datetime

# Definición de pines en formato GPIO
TOGGLE_1 = 2
TOGGLE_2 = 3
LCD_RS = 4
LCD_E = 17
LCD_D4 = 18
LCD_D5 = 22
LCD_D6 = 23
LCD_D7 = 24
Avance = 25
Retroceso = 26

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

print("Puente H")

# Obtener el chip y los pines
chip = gpiod.Chip('/dev/gpiochip4')  # Ajusta si es necesario
pins = {pin: chip.get_line(pin) for pin in [TOGGLE_1, TOGGLE_2, LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, Avance, Retroceso]}

# Configuración de pines (solo una vez)
pins[TOGGLE_1].request(consumer='input', type=gpiod.LINE_REQ_DIR_IN)
pins[TOGGLE_2].request(consumer='input', type=gpiod.LINE_REQ_DIR_IN)

for salida in bits_datos:
    pins[salida].request(consumer='output', type=gpiod.LINE_REQ_DIR_OUT)

pins[Avance].request(consumer='output', type=gpiod.LINE_REQ_DIR_OUT)
pins[Retroceso].request(consumer='output', type=gpiod.LINE_REQ_DIR_OUT)

def lcd_write(bits, mode):
    pins[LCD_RS].set_value(mode)
    pins[LCD_D4].set_value((bits & 0x10) == 0x10)
    pins[LCD_D5].set_value((bits & 0x20) == 0x20)
    pins[LCD_D6].set_value((bits & 0x40) == 0x40)
    pins[LCD_D7].set_value((bits & 0x80) == 0x80)
    lcd_toggle_enable()
    pins[LCD_D4].set_value((bits & 0x01) == 0x01)
    pins[LCD_D5].set_value((bits & 0x02) == 0x02)
    pins[LCD_D6].set_value((bits & 0x04) == 0x04)
    pins[LCD_D7].set_value((bits & 0x08) == 0x08)
    lcd_toggle_enable()

def lcd_toggle_enable():
    sleep(0.0005)
    pins[LCD_E].set_value(1)
    sleep(0.0005)
    pins[LCD_E].set_value(0)
    sleep(0.0005)

def lcd_init():
    lcd_write(0x33, 0)
    lcd_write(0x32, 0)
    lcd_write(0x06, 0)
    lcd_write(0x0C, 0)
    lcd_write(0x28, 0)
    lcd_write(0x01, 0)
    sleep(0.0005)

def lcd_texto(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, 0)
    for i in range(16):
        lcd_write(ord(message[i]), 1)

def LCD(hora):
    lcd_init()
    lcd_texto(hora, 0x80)
    sleep(0.01)

def Movimiento(AR):
    if AR == 1:
        pins[Avance].set_value(1)
        pins[Retroceso].set_value(0)
    elif AR == 0:
        pins[Avance].set_value(0)
        pins[Retroceso].set_value(1)
    else:
        pins[Avance].set_value(0)
        pins[Retroceso].set_value(0)

try:
    while True:
        if pins[TOGGLE_1].get_value() == 0:  # Si TOGGLE_1 está activado
            LCD("Giro izquierda")
            Movimiento(1)
            print("Giro izquierda", pins[TOGGLE_1].get_value(), "|", pins[TOGGLE_2].get_value(), "|", str(datetime.datetime.now()))
        elif pins[TOGGLE_2].get_value() == 0:  # Si TOGGLE_2 está activado
            LCD("Giro derecha")
            Movimiento(0)
            print("Giro derecha, ", pins[TOGGLE_1].get_value(), "|", pins[TOGGLE_2].get_value(), "|", str(datetime.datetime.now()))
        else:
            LCD("Detenido | ECCI")
            print("Detenido", pins[TOGGLE_1].get_value(), "|", pins[TOGGLE_2].get_value(), "|", str(datetime.datetime.now()))
            Movimiento(-1)  # Asegurarse de detener el movimiento si no hay entradas activadas
        sleep(1)

except KeyboardInterrupt:
    pass  # No es necesario limpiar pines con gpiod, ya que el manejador de interrupciones se encarga automáticamente