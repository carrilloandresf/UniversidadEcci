import tkinter as tk  # Importa la librería Tkinter para crear interfaces gráficas
import RPi.GPIO as GPIO  # Importa la librería RPi.GPIO para controlar los pines GPIO de la Raspberry Pi

# Configuración de los pines
led_pin_1 = 27  # Define el pin donde está conectado el primer LED (modo BOARD)
led_pin_2 = 26  # Define el pin donde está conectado el segundo LED (modo BCM)

# Configura el uso de la numeración de los pines en modo BOARD (para led_pin_1) y modo BCM (para led_pin_2)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin_1, GPIO.OUT)  # Configura el pin del primer LED como salida
GPIO.setup(led_pin_2, GPIO.OUT)  # Configura el pin del segundo LED como salida

# Función para encender y apagar el primer LED
def toggle_led_1():
    current_state_1 = GPIO.input(led_pin_1)  # Lee el estado actual del primer LED
    GPIO.output(led_pin_1, not current_state_1)  # Cambia el estado del primer LED (encender/apagar)

# Función para encender y apagar el segundo LED
def toggle_led_2():
    current_state_2 = GPIO.input(led_pin_2)  # Lee el estado actual del segundo LED
    GPIO.output(led_pin_2, not current_state_2)  # Cambia el estado del segundo LED (encender/apagar)

# Configuración de la ventana de Tkinter
root = tk.Tk()  # Crea la ventana principal de Tkinter
root.title("Control de 2 LEDs")  # Título de la ventana

# Botón para encender/apagar el primer LED
led_button_1 = tk.Button(root, text="LED 1", command=toggle_led_1)  # Crea el botón para controlar el primer LED
led_button_1.pack(pady=20)  # Coloca el botón en la ventana con un espacio vertical de 20 píxeles
led_button_1.place(x=50, y=50)  # Ubica el botón en la posición (50, 50) de la ventana

# Botón para encender/apagar el segundo LED
led_button_2 = tk.Button(root, text="LED 2", command=toggle_led_2)  # Crea el botón para controlar el segundo LED
led_button_2.pack(pady=20)  # Coloca el botón en la ventana con un espacio vertical de 20 píxeles
led_button_2.place(x=50, y=100)  # Ubica el botón en la posición (50, 100) de la ventana

# Cierre adecuado de GPIO al salir
def on_closing():
    GPIO.cleanup()  # Limpia los pines GPIO para asegurarse de que estén en estado seguro
    root.quit()  # Cierra la ventana de la aplicación

# Detecta si el usuario cierra la ventana y ejecuta la función 'on_closing' para limpiar los GPIO
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la aplicación
root.mainloop()  # Mantiene la ventana abierta y esperando interacción del usuario
