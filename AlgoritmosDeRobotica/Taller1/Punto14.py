"""
Carga del capacitor:
V(t) = V_in * (1 - exp(-t / (R * C))

Donde:

V(t) es el voltaje a través del capacitor en función del tiempo.
V_in es el voltaje inicial aplicado al capacitor.
R es la resistencia en ohmios.
C es la capacitancia en faradios.
t es el tiempo en segundos.
La fórmula describe cómo el voltaje a través del capacitor aumenta desde 0 hasta V_in conforme el capacitor se carga a través de la resistencia.

Descarga del capacitor:
V(t) = V_in * exp(-t / (R * C))

Donde:

V(t) es el voltaje a través del capacitor en función del tiempo.
V_in es el voltaje inicial del capacitor antes de que comience la descarga.
R es la resistencia en ohmios.
C es la capacitancia en faradios.
t es el tiempo en segundos.
La fórmula describe cómo el voltaje a través del capacitor disminuye desde V_in hacia 0 conforme el capacitor se descarga a través de la resistencia.
"""

import numpy as np
import matplotlib.pyplot as plt

def carga_rc(t, V_in, R, C):
    """
    Calcula el voltaje a través del capacitor durante la carga.
    
    :param t: Tiempo.
    :param V_in: Voltaje inicial.
    :param R: Resistencia.
    :param C: Capacitancia.
    :return: Voltaje a través del capacitor en el tiempo t.
    """
    return V_in * (1 - np.exp(-t / (R * C)))

def descarga_rc(t, V_in, R, C):
    """
    Calcula el voltaje a través del capacitor durante la descarga.
    
    :param t: Tiempo.
    :param V_in: Voltaje inicial.
    :param R: Resistencia.
    :param C: Capacitancia.
    :return: Voltaje a través del capacitor en el tiempo t.
    """
    return V_in * np.exp(-t / (R * C))

def main():
    # Solicitar valores al usuario
    V_in = float(input("Ingrese el voltaje (V): "))
    C = float(input("Ingrese la capacitancia (μF): ")) * 1e-6  # Convertir μF a F
    R = float(input("Ingrese la resistencia (Ω): "))
    
    # Tiempo de simulación
    t = np.linspace(0, 0.005, 500)  # Tiempo de 0 a 5 ms
    
    # Calcular la carga y descarga
    V_carga = carga_rc(t, V_in, R, C)
    V_descarga = descarga_rc(t, V_in, R, C)
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(t, V_carga, label='Carga', color='b')
    plt.plot(t, V_descarga, label='Descarga', color='r')
    plt.title('Carga y Descarga de un Circuito RC')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Voltaje (V)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
