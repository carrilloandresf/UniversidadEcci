import time
import random
from datetime import datetime

while True:
    # Obtener la hora actual
    now = datetime.now()
    hora_actual = now.strftime("%H:%M:%S")
    
    # Imprimir la hora
    print("Hora actual:", hora_actual)
    
    # Generar un intervalo de sleep aleatorio entre 0.5 y 3 segundos
    intervalo_sleep = random.uniform(0.5, 3.0)
    
    # Esperar el intervalo de tiempo generado
    time.sleep(intervalo_sleep)
