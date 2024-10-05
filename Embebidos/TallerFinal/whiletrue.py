import time
import random
from datetime import datetime

# Obtener la hora de inicio del programa
inicio_programa = datetime.now()

def calcular_progreso(inicio):
    # Hora de fin a las 22:00 (10:00 p.m.)
    fin = datetime(inicio.year, inicio.month, inicio.day, 13, 00, 0)
    
    # Calcular el progreso en porcentaje
    total_seconds = (fin - inicio).total_seconds()
    elapsed_seconds = (datetime.now() - inicio).total_seconds()
    progress = min((elapsed_seconds / total_seconds) * 100, 100)  # Limitar al 100%
    return progress

while True:
    # Calcular el progreso actual
    progreso = calcular_progreso(inicio_programa)
    
    # Obtener la hora actual
    hora_actual = datetime.now().strftime("%H:%M:%S")
    
    # Imprimir la hora actual y el progreso en la misma línea
    barra = "#" * int(progreso / 2)  # Ajustar la longitud de la barra
    print(f"\rHora actual: {hora_actual} [{barra:<50}] {progreso:.2f}%", end="")
    
    # Si el progreso alcanza el 100%, finalizar el bucle
    if progreso >= 100:
        print("\n¡El programa ha alcanzado el 100% de progreso!")
        break
    
    # Esperar un intervalo aleatorio entre 0.5 y 3 segundos
    intervalo_sleep = random.uniform(1.0, 2.0)
    time.sleep(intervalo_sleep)
