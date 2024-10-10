import tkinter as tk  # Importa la librería Tkinter para crear interfaces gráficas
import RPi.GPIO as GPIO  # Importa la librería RPi.GPIO para controlar los pines GPIO de la Raspberry Pi

# Configuración de los pines
led_pin = 27  # Define el pin donde está conectado el LED (número de pin en modo BOARD)

# Configura el uso de la numeración de los pines en modo BOARD (basado en la posición física de los pines)
GPIO.setmode(GPIO.BOARD)

# Configura el pin del LED como salida
GPIO.setup(led_pin, GPIO.OUT)

# Función para encender y apagar el LED
def toggle_led():
    current_state = GPIO.input(led_pin)  # Lee el estado actual del pin (encendido o apagado)
    GPIO.output(led_pin, not current_state)  # Cambia el estado del pin (si está encendido, lo apaga y viceversa)

# Configuración de la ventana de Tkinter
root = tk.Tk()  # Crea la ventana principal de Tkinter
root.title("Control de LED")  # Título de la ventana

# Botón para encender/apagar el LED
led_button = tk.Button(root, text="LED_1", command=toggle_led)  # Crea un botón con el texto 'LED_1' y la función 'toggle_led'
led_button.pack(pady=300)  # Coloca el botón en la ventana con un espacio de 300 píxeles en el eje y (vertical)
led_button.place(x=50, y=50)  # Ubica el botón en la posición (50, 50) de la ventana

# Cierre adecuado de GPIO al salir
def on_closing():
    GPIO.cleanup()  # Limpia los pines GPIO para asegurarse de que estén en estado seguro
    root.quit()  # Cierra la ventana de la aplicación

# Detecta si el usuario cierra la ventana y ejecuta la función 'on_closing' para limpiar los GPIO
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la aplicación
root.mainloop()  # Mantiene la ventana abierta y esperando interacción del usuario
