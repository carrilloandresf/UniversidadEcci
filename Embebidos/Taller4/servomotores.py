import gpiod
from time import sleep

# Configuración del chip GPIO y la línea del pin 13 (gpiochip4, línea 13)
chip = gpiod.Chip('gpiochip4')
pwmgpio13 = 14  # Línea GPIO 13

# Configuración del PWM manual (en este caso, usaremos sleep para simular el PWM)
frecuencia = 50  # Frecuencia en Hz
periodo = 1.0 / frecuencia  # Período del ciclo en segundos

# Cálculo de duty cycle en función del ángulo
def porcentaje(angulo):
    if angulo > 180 or angulo < 0:
        return False

    comienzo = 4
    final = 12.5
    radio = (final - comienzo) / 180
    return comienzo + (radio * angulo)

# Establecer línea de salida
linea = chip.get_line(pwmgpio13)

# Solicitar la línea para salida
linea.request(consumer="pwm_control", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        # Simular el PWM para ángulo 0°
        print("0°")
        duty_cycle_0 = porcentaje(0) / 100  # Convertir a fracción
        linea.set_value(1)  # Encender GPIO
        sleep(duty_cycle_0 * periodo)
        linea.set_value(0)  # Apagar GPIO
        sleep((1 - duty_cycle_0) * periodo)

        print("180°")
        # Simular el PWM para ángulo 180°
        duty_cycle_180 = porcentaje(180) / 100  # Convertir a fracción
        linea.set_value(1)
        sleep(duty_cycle_180 * periodo)
        linea.set_value(0)
        sleep((1 - duty_cycle_180) * periodo)

        # Simular el PWM para ángulo 90°
        print("90°")
        duty_cycle_90 = porcentaje(90) / 100
        linea.set_value(1)
        sleep(duty_cycle_90 * periodo)
        linea.set_value(0)
        sleep((1 - duty_cycle_90) * periodo)

except KeyboardInterrupt:
    pass

finally:
    linea.set_value(0)  # Asegurarse de que el pin esté apagado
    chip.close()
