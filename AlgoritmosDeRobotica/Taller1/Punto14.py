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
    
    # Tiempo de simulación extendido hasta 5 tau
    tau = R * C
    t = np.linspace(0, 5 * tau, 500)
    
    # Calcular la carga y descarga
    V_carga = carga_rc(t, V_in, R, C)
    V_descarga = descarga_rc(t, V_in, R, C)
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(t, V_carga, label='Carga', color='b')
    plt.plot(t, V_descarga, label='Descarga', color='r')
    plt.title('Carga y Descarga de un Circuito RC hasta 5τ')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Voltaje (V)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
