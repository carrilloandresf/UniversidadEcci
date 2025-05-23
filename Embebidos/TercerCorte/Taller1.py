import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as GPIO

# Configuración de los GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definir los pines GPIO para el puente H y el zumbador
MOTOR_LEFT = 18
MOTOR_RIGHT = 17
BUZZER = 23

# Configurar los pines como salidas
GPIO.setup(MOTOR_LEFT, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Variables de estado para los botones de giro
motor_left_state = False
motor_right_state = False

# Funciones para controlar el motor y el zumbador
def toggle_left():
    global motor_left_state
    if motor_left_state:
        stop_motor()
        motor_left_state = False
    else:
        GPIO.output(MOTOR_LEFT, GPIO.HIGH)
        GPIO.output(MOTOR_RIGHT, GPIO.LOW)
        motor_left_state = True

def toggle_right():
    global motor_right_state
    if motor_right_state:
        stop_motor()
        motor_right_state = False
    else:
        GPIO.output(MOTOR_LEFT, GPIO.LOW)
        GPIO.output(MOTOR_RIGHT, GPIO.HIGH)
        motor_right_state = True

def stop_motor():
    GPIO.output(MOTOR_LEFT, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT, GPIO.LOW)

def toggle_buzzer():
    if GPIO.input(BUZZER):
        GPIO.output(BUZZER, GPIO.LOW)
    else:
        GPIO.output(BUZZER, GPIO.HIGH)

def exit_program():
    stop_motor()
    GPIO.cleanup()
    root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Puente-H y Zumbador")

# Mostrar mensaje emergente
messagebox.showinfo("Bienvenida", "Profe te amo")

# Crear los botones con colores personalizados
btn_left = tk.Button(root, text="Girar Izquierda", command=toggle_left, bg="#FF9999", fg="white", font=("Arial", 12, "bold"))
btn_right = tk.Button(root, text="Girar Derecha", command=toggle_right, bg="#99CCFF", fg="white", font=("Arial", 12, "bold"))
btn_buzzer = tk.Button(root, text="Encender/Apagar Zumbador", command=toggle_buzzer, bg="#FFD700", fg="black", font=("Arial", 12, "bold"))
btn_exit = tk.Button(root, text="Salir", command=exit_program, bg="#FF6666", fg="white", font=("Arial", 12, "bold"))

# Crear la caja de texto
text_box = tk.Entry(root, width=30, font=("Arial", 12))

# Colocar los widgets en la ventana
btn_left.grid(row=0, column=0, padx=10, pady=10)
btn_buzzer.grid(row=0, column=1, padx=10, pady=10)
btn_right.grid(row=0, column=2, padx=10, pady=10)
btn_exit.grid(row=1, column=1, padx=10, pady=10)
text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Configuración del evento de cierre de ventana
root.protocol("WM_DELETE_WINDOW", exit_program)

# Ejecutar la aplicación
root.mainloop()
