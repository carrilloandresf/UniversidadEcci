import tkinter as tk
from datetime import datetime
import threading
import time
import board
import busio
import adafruit_ahtx0
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306

# Configuración de la comunicación I2C y sensor AHTx0
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

# Configuración de la pantalla OLED
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Ruta del archivo log
log_file = "log_humedad.txt"

def log_data(temperature, humidity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{timestamp} - TEMP: {temperature:.2f}°C, HUM: {humidity:.2f}%\n")

# Función para actualizar la pantalla
def update_display():
    last_log_time = time.time()
    while True:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        
        temperature_label.config(text=f"Temp: {temperature:.2f}°C")
        humidity_label.config(text=f"Humedad: {humidity:.2f}%")
        
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), f"Temp: {temperature:.2f} C", font=font, fill=255)
        draw.text((0, 15), f"Humedad: {humidity:.2f} %", font=font, fill=255)
        disp.image(image)
        disp.display()

        if time.time() - last_log_time >= 60:
            log_data(temperature, humidity)
            last_log_time = time.time()

        time.sleep(0.5)

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Monitor de Temp. y Humedad")
root.geometry("400x100")

frame = tk.Frame(root)
frame.pack(pady=20)

temperature_label = tk.Label(frame, text="Temp: -- °C", font=("Helvetica", 14))
temperature_label.grid(row=0, column=0, padx=10)

humidity_label = tk.Label(frame, text="Humedad: -- %", font=("Helvetica", 14))
humidity_label.grid(row=0, column=1, padx=10)

data_thread = threading.Thread(target=update_display, daemon=True)
data_thread.start()

# Ejecutar la interfaz Tkinter
root.mainloop()