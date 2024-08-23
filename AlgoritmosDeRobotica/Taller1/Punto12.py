import matplotlib.pyplot as plt
import numpy as np

def resistencia_pt100(temperatura):
    """
    Calcula la resistencia del sensor PT100 en función de la temperatura
    utilizando las fórmulas específicas para temperaturas mayores o iguales a 0°C
    y menores a 0°C.
    
    :param temperatura: Temperatura en grados Celsius.
    :return: Resistencia en ohmios.
    """
    R0 = 100  # Resistencia a 0°C
    A = 3.9083e-3  # Coeficiente A en °C⁻¹
    B = -5.775e-7  # Coeficiente B en °C⁻²
    C = -4.183e-12  # Coeficiente C en °C⁻⁴, solo para t < 0°C
    
    if temperatura >= 0:
        return R0 * (1 + A * temperatura + B * temperatura**2)
    else:
        return R0 * (1 + A * temperatura + B * temperatura**2 + C * (temperatura - 100) * temperatura**3)

def main():
    # Generar un rango de temperaturas de -200°C a 200°C
    temperaturas = np.linspace(-200, 200, 400)
    resistencias = [resistencia_pt100(t) for t in temperaturas]
    
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
