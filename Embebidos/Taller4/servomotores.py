import gpiod
from time import sleep

# Variables para flat
FLAT1 = 0
FLAT2 = 0

# Pines en el gpiochip4 (ajusta según el chip que estés utilizando)
chip = gpiod.Chip('gpiochip4')

# Pines para los servos
SERVO_1 = 13
SERVO_2 = 16

# Pines para los pulsadores
PULSE_1 = 4
PULSE_2 = 7

# Pines para el LCD
LCD_RS = 10
LCD_E = 9
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

# Solicitar acceso a los pines con gpiod
lines = {
    'servo_1': chip.get_line(SERVO_1),
    'servo_2': chip.get_line(SERVO_2),
    'pulse_1': chip.get_line(PULSE_1),
    'pulse_2': chip.get_line(PULSE_2),
    'lcd_rs': chip.get_line(LCD_RS),
    'lcd_e': chip.get_line(LCD_E),
    'lcd_d4': chip.get_line(LCD_D4),
    'lcd_d5': chip.get_line(LCD_D5),
    'lcd_d6': chip.get_line(LCD_D6),
    'lcd_d7': chip.get_line(LCD_D7),
}

# Configurar líneas como salida o entrada
for name in ['servo_1', 'servo_2', 'lcd_rs', 'lcd_e', 'lcd_d4', 'lcd_d5', 'lcd_d6', 'lcd_d7']:
    lines[name].request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT)

for name in ['pulse_1', 'pulse_2']:
    lines[name].request(consumer=name, type=gpiod.LINE_REQ_DIR_IN)

# Función para calcular el duty cycle en función del ángulo
def porcentaje(angulo):
    comienzo = 2.5  # Valor de PWM para -90 grados
    final = 12.5  # Valor de PWM para +90 grados
    radio = (final - comienzo) / 180
    return comienzo + (radio * (angulo + 90))

# Función para escribir en el LCD
def lcd_write(bits, mode):
    lines['lcd_rs'].set_value(mode)
    lines['lcd_d4'].set_value(bits & 0x10 == 0x10)
    lines['lcd_d5'].set_value(bits & 0x20 == 0x20)
    lines['lcd_d6'].set_value(bits & 0x40 == 0x40)
    lines['lcd_d7'].set_value(bits & 0x80 == 0x80)
    lcd_toggle_enable()
    lines['lcd_d4'].set_value(bits & 0x01 == 0x01)
    lines['lcd_d5'].set_value(bits & 0x02 == 0x02)
    lines['lcd_d6'].set_value(bits & 0x04 == 0x04)
    lines['lcd_d7'].set_value(bits & 0x08 == 0x08)
    lcd_toggle_enable()

def lcd_toggle_enable():
    sleep(0.0005)
    lines['lcd_e'].set_value(True)
    sleep(0.0005)
    lines['lcd_e'].set_value(False)
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

def LCD(message1, message2):
    lcd_init()
    lcd_texto(message1, 0x80)  # Primera línea
    lcd_texto(message2, 0xC0)  # Segunda línea
    sleep(0.01)

# Función para mover el servo
def mover_servo(line, angulo):
    duty_cycle = porcentaje(angulo)
    # Aquí debes implementar el control PWM, ya que gpiod no tiene directamente PWM.
    # Se puede usar una librería como pigpio para generar PWM, o manejar con delays el control de tiempo.
    print(f"Mover {line} a ángulo {angulo} con ciclo de trabajo {duty_cycle}")
    # Implementa el movimiento real del servo

try:
    # Estado inicial
    estado_servo_1 = "Stop"
    estado_servo_2 = "Stop"
    
    while True:
        # Control para el Servo 1
        if lines['pulse_1'].get_value() == 1:
            estado_servo_1 = "Servo_1 giro 90 grados"
            mover_servo('servo_1', 90)
            FLAT1 = 1
        elif lines['pulse_1'].get_value() == 0 and FLAT1 == 1:
            estado_servo_1 = "Servo_1 giro -90 grados"
            mover_servo('servo_1', -90)
            FLAT1 = 0
        else:
            estado_servo_1 = "Servo_1 Stop"

        # Control para el Servo 2
        if lines['pulse_2'].get_value() == 1:
            estado_servo_2 = "Servo_2 giro 90 grados"
            mover_servo('servo_2', 90)
            FLAT2 = 1
        elif lines['pulse_2'].get_value() == 0 and FLAT2 == 1:
            estado_servo_2 = "Servo_2 giro -90 grados"
            mover_servo('servo_2', -90)
            FLAT2 = 0
        else:
            estado_servo_2 = "Servo_2 Stop"

        # Mostrar en el LCD
        LCD(estado_servo_1, estado_servo_2)
        sleep(0.5)  # Pausa antes de la siguiente actualización

except KeyboardInterrupt:
    # Limpieza de los GPIO
    chip.close()
