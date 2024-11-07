# Importación de librerías necesarias
import time
import board
import adafruit_ahtx0
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

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

# Configuración de Tkinter
root = tk.Tk()
root.title("Lectura de Temperatura y Humedad")
root.geometry("300x100")

# Variables de Tkinter para actualizar los valores
temp_var = tk.StringVar()
hum_var = tk.StringVar()
temp_label = tk.Label(root, textvariable=temp_var, font=("Helvetica", 16))
hum_label = tk.Label(root, textvariable=hum_var, font=("Helvetica", 16))
temp_label.pack(pady=10)
hum_label.pack(pady=10)

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

# Función para actualizar la pantalla OLED y la interfaz de Tkinter
def actualizar_datos():
    # Leer temperatura y humedad del sensor
    temperatura = sensor.temperature
    humedad = sensor.relative_humidity

    # Actualizar los valores en la interfaz de Tkinter
    temp_var.set(f"Temperatura: {temperatura:.1f} C")
    hum_var.set(f"Humedad: {humedad:.1f} %")
    
    # Limpiar la pantalla OLED
    disp.clear()
    
    # Limpiar la imagen previa en el buffer
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
    
    # Dibujar el texto en el buffer de la pantalla OLED
    draw.text((0, 0), f"Temperatura: {temperatura:.1f} C", fill=255)
    draw.text((0, 16), f"Humedad: {humedad:.1f} %", fill=255)

    # Enviar la imagen generada al buffer de la pantalla OLED
    disp.image(image)
    disp.display()

    # Programar la próxima actualización en 2 segundos
    root.after(2000, actualizar_datos)

# Iniciar la actualización de datos
actualizar_datos()

# Iniciar el loop de Tkinter
root.mainloop()