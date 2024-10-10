import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as GPIO

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 24
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Inicializamos el estado del LED como apagado
led_state = False

# Función para cambiar el estado del LED
def toggle_led():
    global led_state
    if led_state:
        GPIO.output(LED_PIN, GPIO.LOW)
        btn_led.config(text="Encender LED")
        led_state = False
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)
        btn_led.config(text="Apagar LED")
        led_state = True

# Función para cerrar la ventana y limpiar los GPIO
def close_window():
    GPIO.cleanup()
    window.quit()

# Crear la ventana principal
window = tk.Tk()
window.title("Control de LED con Tkinter")

# Botón para encender/apagar el LED
btn_led = tk.Button(window, text="Encender LED", command=toggle_led, width=20, height=2)
btn_led.pack(pady=20)

# Botón para salir de la aplicación
btn_exit = tk.Button(window, text="Salir", command=close_window, width=20, height=2)
btn_exit.pack(pady=20)

# Ejecutar la ventana principal
window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()
