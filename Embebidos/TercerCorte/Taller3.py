# Importación de librerías necesarias
import time
import board
import adafruit_ahtx0
import Adafruit_SSD1306
import Adafruit_GPIO.I2C as I2C
from PIL import Image, ImageDraw, ImageFont

# Configuración de la pantalla OLED y dirección I2C
RST = None  # Raspberry Pi configura el pin de reset de la OLED
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)

# Inicialización de la pantalla
disp.begin()   # Inicializa la pantalla OLED
disp.clear()   # Limpia el buffer de la pantalla
disp.display() # Muestra el buffer vacío en la pantalla

# Crear imagen en blanco con el modo '1' (1 bit de color)
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Configuración del sensor AHT20
i2c = board.I2C()  # Usa el bus I2C por defecto
sensor = adafruit_ahtx0.AHTx0(i2c)

# Definición de los bitmaps para cada letra
bitmap_E = [
    0b1111111111,
    0b1100000000,
    0b1100000000,
    0b1100000000,
    0b1111111111,
    0b1111111111,
    0b1100000000,
    0b1100000000,
    0b1100000000,
    0b1111111111,
]

bitmap_C = [
    0b0111111110,
    0b1100000011,
    0b1000000001,
    0b1000000000,
    0b1000000000,
    0b1000000000,
    0b1000000001,
    0b1100000011,
    0b0111111110,
    0b0000000000,
]

bitmap_I = [
    0b1111111111,
    0b0001100000,
    0b0001100000,
    0b0001100000,
    0b0001100000,
    0b0001100000,
    0b0001100000,
    0b0001100000,
    0b1111111111,
    0b0000000000,
]

# Función para dibujar letras en la pantalla OLED
def draw_ecci(x, y, bitmap):
    for i in range(10):
        for j in range(10):
            if (bitmap[i] >> (9 - j)) & 1:
                draw.point((x + j, y + i), fill=1)

# Dibujar las letras 'E', 'C', 'C', 'I' en las posiciones correspondientes
draw_ecci(20, 10, bitmap_E)
draw_ecci(40, 10, bitmap_C)
draw_ecci(60, 10, bitmap_C)
draw_ecci(80, 10, bitmap_I)

# Bucle para mostrar temperatura y humedad continuamente
while True:
    # Leer temperatura y humedad del sensor
    temperatura = sensor.temperature
    humedad = sensor.relative_humidity

    # Limpiar la imagen previa
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    
    # Dibujar el texto en el buffer de la pantalla
    draw.text((0, 0), f"Temperatura: {temperatura:.1f} C", fill=255)
    draw.text((0, 16), f"Humedad: {humedad:.1f} %", fill=255)

    # Enviar la imagen generada al buffer de la pantalla OLED
    disp.image(image)
    disp.display()

    # Espera de 2 segundos antes de la siguiente lectura
    time.sleep(2)