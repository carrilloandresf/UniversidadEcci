import matplotlib.pyplot as plt
import numpy as np

def resistencia_pt100(temperatura):
    """
    Calcula la resistencia del sensor PT100 en función de la temperatura.
    
    :param temperatura: Temperatura en grados Celsius.
    :return: Resistencia en ohmios.
    """
    resistencia_0 = 100  # Resistencia a 0°C
    coeficiente = 0.385  # Coeficiente de temperatura en ohmios/°C
    return resistencia_0 * (1 + coeficiente * temperatura)

def main():
    # Generar un rango de temperaturas de -200°C a 200°C
    temperaturas = np.linspace(-200, 200, 400)
    resistencias = resistencia_pt100(temperaturas)
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(temperaturas, resistencias, label='Sensor PT100', color='b')
    plt.title('Comportamiento del Sensor PT100')
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Resistencia (ohmios)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
