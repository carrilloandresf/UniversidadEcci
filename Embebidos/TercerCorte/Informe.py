import tkinter as tk
import board
import busio
import adafruit_ahtx0
from datetime import datetime
import time
import threading

# Configuración de la comunicación I2C y sensor AHTx0
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

# Ruta del archivo log
log_file = "log_temperatura_humedad.txt"

# Función para escribir datos en el archivo log
def log_data(temperature, humidity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{timestamp} - Temperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%\n")

# Función para actualizar los datos en la interfaz y log cada minuto
def update_data():
    while True:
        # Obtener temperatura y humedad del sensor
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        
        # Actualizar los labels en la interfaz de Tkinter
        temperature_label.config(text=f"Temperatura: {temperature:.2f}°C")
        humidity_label.config(text=f"Humedad: {humidity:.2f}%")
        
        # Escribir en el log cada minuto
        log_data(temperature, humidity)
        
        # Esperar 1 minuto antes de la próxima actualización
        time.sleep(60)

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Monitor de Temperatura y Humedad")
root.geometry("300x150")

temperature_label = tk.Label(root, text="Temperatura: -- °C", font=("Helvetica", 16))
temperature_label.pack(pady=10)

humidity_label = tk.Label(root, text="Humedad: -- %", font=("Helvetica", 16))
humidity_label.pack(pady=10)

# Iniciar el thread para actualizar datos y evitar que bloquee la interfaz
data_thread = threading.Thread(target=update_data, daemon=True)
data_thread.start()

# Ejecutar la interfaz Tkinter
root.mainloop()
