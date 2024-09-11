import gpiod
from time import sleep

# Definir el chip GPIO (gpiochip4)
chip = gpiod.Chip('gpiochip4')

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

def setup_lines():
    global toggle_1_line, toggle_2_line, lcd_lines, avance_line, retroceso_line
    
    # Configuración de pines
    toggle_1_line = chip.get_line(TOGGLE_1)
    toggle_2_line = chip.get_line(TOGGLE_2)
    
    # Configuración de pines para LCD
    lcd_lines = [chip.get_line(pin) for pin in bits_datos + [LCD_E]]
    
    # Configuración de pines para motores
    avance_line = chip.get_line(Avance)
    retroceso_line = chip.get_line(Retroceso)
    
    # Liberar líneas si ya están solicitadas
    for line in [toggle_1_line, toggle_2_line] + lcd_lines + [avance_line, retroceso_line]:
        if line.is_requested():
            line.release()
    
    # Solicitar líneas GPIO
    try:
        toggle_1_line.request(consumer="toggle_check", type=gpiod.LINE_REQ_DIR_IN)
        toggle_2_line.request(consumer="toggle_check", type=gpiod.LINE_REQ_DIR_IN)
        
        for line in lcd_lines:
            line.request(consumer="lcd_program", type=gpiod.LINE_REQ_DIR_OUT)
        
        avance_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
        retroceso_line.request(consumer="motor_control", type=gpiod.LINE_REQ_DIR_OUT)
    
    except Exception as e:
        print(f"Error al solicitar líneas GPIO: {e}")

def release_lines():
    global toggle_1_line, toggle_2_line, lcd_lines, avance_line, retroceso_line
    
    # Liberar líneas GPIO
    for line in [toggle_1_line, toggle_2_line] + lcd_lines + [avance_line, retroceso_line]:
        if line.is_requested():
            line.release()

# Configuración de pines (solo una vez)
setup_lines()

def lcd_write(bits, mode):
    values = [
        mode,
        (bits & 0x10) >> 4,
        (bits & 0x20) >> 5,
        (bits & 0x40) >> 6,
        (bits & 0x80) >> 7
    ]
    for line, value in zip(lcd_lines, values):
        line.set_value(value)
    lcd_toggle_enable()

    values = [
        mode,
        (bits & 0x01),
        (bits & 0x02) >> 1,
        (bits & 0x04) >> 2,
        (bits & 0x08) >> 3
    ]
    for line, value in zip(lcd_lines, values):
        line.set_value(value)
    lcd_toggle_enable()

def lcd_toggle_enable():
    line = chip.get_line(LCD_E)
    line.set_value(1)
    sleep(0.0005)
    line.set_value(0)
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
        # Lee el valor de las líneas ya solicitadas
        if toggle_1_line.get_value() == 1:  # Si TOGGLE_1 está activado
            LCD("Giro izquierda")
            Movimiento(1)
        elif toggle_2_line.get_value() == 1:  # Si TOGGLE_2 está activado
            LCD("Giro derecha")
            Movimiento(0)
        else:
            LCD("Detenido | ECCI")
            Movimiento(-1)  # Asegurarse de detener el movimiento si no hay entradas activadas
        sleep(0.5)

except KeyboardInterrupt:
    # Libera las líneas GPIO antes de salir
    release_lines()
    print("Interrupción del teclado detectada. Limpieza y salida.")
