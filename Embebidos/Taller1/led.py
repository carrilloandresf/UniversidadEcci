import gpiod
import time

# Lista de pines GPIO a utilizar (del 2 al 27)
pins = list(range(2, 28))

try:
    # Configurar el chip GPIO
    chip = gpiod.Chip('gpiochip4')

    # Crear una lista de líneas para los pines
    lines = [chip.get_line(pin) for pin in pins]

    # Configurar cada línea como salida
    for line in lines:
        line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

    # Encender los LEDs uno por uno con un retardo de 0.5 segundos
    for line in lines:
        line.set_value(1)  # Encender el LED
        time.sleep(0.5)    # Esperar 0.5 segundos

except Exception as e:
    # Mostrar cualquier error que ocurra
    print(f"Ocurrió un error: {e}")

except KeyboardInterrupt:
    # Manejar la interrupción con Ctrl+C
    print("Programa interrumpido por el usuario.")

finally:
    # Liberar las líneas al final
    for line in lines:
        line.release()
