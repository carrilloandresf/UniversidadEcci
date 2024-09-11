import gpiod
from time import sleep

# Definir el chip GPIO (gpiochip4)
chip = gpiod.Chip('gpiochip4')

# Definición de pines en formato GPIO (BCM)
TOGGLE_1 = 2    # GPIO 5
TOGGLE_2 = 3    # GPIO 6
LCD_RS = 4     # GPIO 10
LCD_E = 17       # GPIO 9
LCD_D4 = 27     # GPIO 22
LCD_D5 = 22     # GPIO 23
LCD_D6 = 10     # GPIO 24
LCD_D7 = 9     # GPIO 25
Avance = 11     # GPIO 17
Retroceso = 18  # GPIO 18

bits_datos = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

# Configuración de pines (solo una vez)
def setup_output(pins):
    lines = chip.get_lines(pins)
    lines.request(consumer="lcd_program", type=gpiod.LINE_REQ_DIR_OUT)

def setup_input(pins):
    lines = chip.get_lines(pins)
    lines.request(consumer="lcd_program", type=gpiod.LINE_REQ_DIR_IN)

setup_input([TOGGLE_1, TOGGLE_2])
setup_output(bits_datos)
setup_output([Avance, Retroceso])

# Función para escribir en el LCD
def lcd_write(bits, mode):
    values = [
        mode,
        (bits & 0x10) >> 4,
        (bits & 0x20) >> 5,
        (bits & 0x40) >> 6,
        (bits & 0x80) >> 7
    ]
    lines = chip.get_lines([LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7])
    lines.set_values(values)
    lcd_toggle_enable()

    values = [
        mode,
        (bits & 0x01),
        (bits & 0x02) >> 1,
        (bits & 0x04) >> 2,
        (bits & 0x08) >> 3
    ]
    lines.set_values(values)
    lcd_toggle_enable()

# Función para activar/desactivar el pin de habilitación del LCD
def lcd_toggle_enable():
    line = chip.get_line(LCD_E)
    line.request(consumer="lcd_program", type=gpiod.LINE_REQ_DIR_OUT)
    sleep(0.0005)
    line.set_value(1)
    sleep(0.0005)
    line.set_value(0)
    sleep(0.0005)

# Inicialización del LCD
def lcd_init():
    lcd_write(0x33, 0)
    lcd_write(0x32, 0)
    lcd_write(0x06, 0)
    lcd_write(0x0C, 0)
    lcd_write(0x28, 0)
    lcd_write(0x01, 0)
    sleep(0.0005)

# Función para mostrar texto en el LCD
def lcd_texto(message, line):
    message = message.ljust(16, " ")
    lcd_write(line, 0)
    for i in range(16):
        lcd_write(ord(message[i]), 1)

# Función para controlar el LCD
def LCD(hora):
    lcd_init()
    lcd_texto(hora, 0x80)
    sleep(0.01)

# Función para controlar movimiento (Avance y Retroceso)
def Movimiento(AR):
    avance_line = chip.get_line(Avance)
    retroceso_line = chip.get_line(Retroceso)
    avance_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
    retroceso_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)

    if AR == 1:
        avance_line.set_value(1)
        retroceso_line.set_value(0)
    elif AR == 0:
        avance_line.set_value(0)
        retroceso_line.set_value(1)
    else:
        avance_line.set_value(0)
        retroceso_line.set_value(0)

try:
    while True:
        toggle_1_line = chip.get_line(TOGGLE_1)
        toggle_2_line = chip.get_line(TOGGLE_2)
        toggle_1_line.request(consumer="toggle_check", type=gpiod.LINE_REQ_DIR_IN)
        toggle_2_line.request(consumer="toggle_check", type=gpiod.LINE_REQ_DIR_IN)

        if toggle_1_line.get_value() == 1:  # Si TOGGLE_1 está activado
            LCD("Giro izquierda")
            Movimiento(1)
        elif toggle_2_line.get_value() == 1:  # Si TOGGLE_2 está activado
            LCD("Giro derecha")
            Movimiento(0)
        else:
            LCD("Detenido | ECCI")
            Movimiento(-1)  # Detener movimiento si no hay entradas activadas
        sleep(0.5)

except KeyboardInterrupt:
    pass  # El cleanup en gpiod no es necesario como en RPi.GPIO
