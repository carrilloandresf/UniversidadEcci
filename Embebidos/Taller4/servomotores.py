import gpiod
from time import sleep

# Configuración del chip GPIO y la línea del pin 13 (gpiochip4, línea 13)
chip = gpiod.Chip('gpiochip4')
pwmgpio13 = 14  # Línea GPIO 13

# Configuración de la frecuencia del PWM
frecuencia = 50  # Frecuencia en Hz
periodo = 1.0 / frecuencia  # Período del ciclo en segundos

# Función para calcular el duty cycle en función del ángulo
def porcentaje(angulo):
    if angulo > 180 or angulo < 0:
        return False

    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    return comienzo + (radio * angulo)

# Solicitar la línea GPIO para salida
linea = chip.get_line(pwmgpio13)
linea.request(consumer="pwm_control", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:  # Bucle infinito
        # Simular el PWM para ángulo 0°
        duty_cycle_0 = porcentaje(0) / 100  # Convertir a fracción
        print("Ángulo: 0°")
        linea.set_value(1)
        sleep(duty_cycle_0 * periodo)
        linea.set_value(0)
        sleep((1 - duty_cycle_0) * periodo)
        sleep(3)  # Esperar 3 segundos entre movimientos

        # Simular el PWM para ángulo 180°
        duty_cycle_180 = porcentaje(180) / 100
        print("Ángulo: 180°")
        linea.set_value(1)
        sleep(duty_cycle_180 * periodo)
        linea.set_value(0)
        sleep((1 - duty_cycle_180) * periodo)
        sleep(3)  # Esperar 3 segundos entre movimientos

        # Simular el PWM para ángulo 90°
        duty_cycle_90 = porcentaje(90) / 100
        print("Ángulo: 90°")
        linea.set_value(1)
        sleep(duty_cycle_90 * periodo)
        linea.set_value(0)
        sleep((1 - duty_cycle_90) * periodo)
        sleep(3)  # Esperar 3 segundos entre movimientos

except KeyboardInterrupt:
    pass

finally:
    linea.set_value(0)  # Asegurarse de apagar la línea
    chip.close()
