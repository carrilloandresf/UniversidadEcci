import spidev
import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configuración del SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Definición de pines
in_Entrada = 4  
in_Salida = 6  
parking_1 = 27
parking_2 = 7
parking_3 = 15

# Movimiento MotorDC
Avance = 17
Retroceso = 18

# Pines del motor paso a paso
BitMot0 = 12
BitMot1 = 13
BitMot2 = 16
BitMot3 = 19
motor_pins = [BitMot0, BitMot1, BitMot2, BitMot3]

# Pines de la LCD
LCD_RS = 5
LCD_E = 26
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

# Pin del servomotor
SERVO_PIN = 20

# Buzzer de cambios
Buzzer_PIN = 21

LED = 14

# Configuración de pines de entrada y salida
GPIO.setup(in_Entrada, GPIO.IN)
GPIO.setup(in_Salida, GPIO.IN)
GPIO.setup(parking_1, GPIO.IN)
GPIO.setup(parking_2, GPIO.IN)
GPIO.setup(parking_3, GPIO.IN)
GPIO.setup(Avance, GPIO.OUT)
GPIO.setup(Retroceso, GPIO.OUT)
GPIO.setup(Buzzer_PIN, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)

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
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Funciones para controlar el movimiento del motor paso a paso
def set_step(step):
    for pin in range(4):
        GPIO.output(motor_pins[pin], step[pin])

def avanzarMotorPasoAPaso(steps, delay=0.01):
    for _ in range(steps):
        for step in STEP_SEQUENCE:
            set_step(step)
            sleep(delay)

def retrocederMotorPasoAPaso(steps, delay=0.01):
    for _ in range(steps):
        for step in reversed(STEP_SEQUENCE):
            set_step(step)
            sleep(delay)

# Funciones para controlar la pantalla LCD
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

# Funciones para leer sensores
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_temp(data, places):
    voltage = (data * 3.3) / 1023
    temp = voltage * 100
    return round(temp, places)

def convert_light(data):
    return data

# Funciones para controlar actuadores
def activar_avance():
    GPIO.output(Avance, True)
    GPIO.output(Retroceso, False)

def activar_retroceso():
    GPIO.output(Avance, False)
    GPIO.output(Retroceso, True)

def detener_motor_dc():
    GPIO.output(Avance, False)
    GPIO.output(Retroceso, False)

def mover_servo(angulo):
    if 0 <= angulo <= 180:
        duty_cycle = 2 + (angulo / 18)
        servo.ChangeDutyCycle(duty_cycle)
        sleep(0.05)
    else:
        print("angulo fuera de rango: debe estar entre 0 y 180 grados")

def activar_buzzer():
    GPIO.output(Buzzer_PIN, True)
    sleep(0.3)
    GPIO.output(Buzzer_PIN, False)

# Inicializa la pantalla LCD al inicio
lcd_init()

lcd_text("UNIVERSIDAD ECCI", 0x80)
lcd_text("Sistemas Embebidos", 0xC0)

sleep(1)

try:
    while True:
        temperature = None
        light = None
        vEntrada = GPIO.input(in_Entrada)  
        vSalida = GPIO.input(in_Salida)
        vParking1 = GPIO.input(parking_1)
        vParking2 = GPIO.input(parking_2)
        vParking3 = GPIO.input(parking_3)

        # Imprimir todas las variables por consola
        print(f"Entrada: {vEntrada}, Salida: {vSalida}, Parking1: {vParking1}, Parking2: {vParking2}, Parking3: {vParking3}")

        # Leer el canal 0 donde está conectado el LM35
        temp_data = read_channel(0)
        temperature = convert_temp(temp_data, 2)

        # Leer el canal 1 donde está conectada la Fotoresistencia
        light_data = read_channel(1)
        light = convert_light(light_data)

        # Mostrar en la pantalla LCD
        lcd_text(f"T:{temperature:.2f}C|L:{light}", 0xC0)
        Parqueadores = (1 if vParking1 == 0 else 0) + (1 if vParking2 == 0 else 0) + (1 if vParking3 == 0 else 0)
        lcd_text(f"PARQUEADEROS: {Parqueadores}", 0x80)

        # Lógica para apertura y cierre de puertas
        if GPIO.input(in_Entrada) and Parqueadores > 0:
            print("Carro en entrada")
            activar_buzzer()
            avanzarMotorPasoAPaso(4)
            while GPIO.input(in_Entrada):
                lcd_text("BIENVENIDO,", 0x80)
                lcd_text(f"DISPONIBLES: {Parqueadores}", 0xC0)
                sleep(2)
            activar_buzzer()
            retrocederMotorPasoAPaso(4)
            lcd_text("ESPERE, VEHICULO", 0x80)
            lcd_text("INGRESANDO...", 0xC0)
            sleep(2)

        if GPIO.input(in_Entrada) and Parqueadores == 0:
            activar_buzzer()

        if GPIO.input(in_Salida):
            print("Carro en salida")
            activar_buzzer()
            mover_servo(90)
            while GPIO.input(in_Salida):
                sleep(1)
            mover_servo(0)

        if temperature is not None and temperature > 30:
            activar_avance()
        else:
            detener_motor_dc()

        if light is not None and light < 100:
            GPIO.output(LED, True)
        else:
            GPIO.output(LED, False)

except KeyboardInterrupt:
    detener_motor_dc()
    servo.stop()
    GPIO.cleanup()
