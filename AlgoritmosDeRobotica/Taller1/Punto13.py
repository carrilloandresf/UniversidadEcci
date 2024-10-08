import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def tipo_sistema(zeta):
    """
    Determina el tipo de sistema basado en el coeficiente de amortiguamiento.
    
    :param zeta: Coeficiente de amortiguamiento.
    :return: Tipo de sistema.
    """
    if zeta < 1:
        return "Subamortiguado"
    elif zeta == 1:
        return "Críticamente amortiguado"
    else:
        return "Sobreamortiguado"

def main():
    # Solicitar coeficientes al usuario
    K = float(input("Ingrese el coeficiente de ganancia (K): "))
    omega_n = float(input("Ingrese la frecuencia natural (omega_n): "))
    zeta = float(input("Ingrese el coeficiente de amortiguamiento (zeta): "))
    
    # Crear la función de transferencia
    num = [K * omega_n**2]  # Numerador con el coeficiente K
    den = [1, 2*zeta*omega_n, omega_n**2]
    
    sistema = signal.TransferFunction(num, den)
    
    # Generar la respuesta al escalón
    tiempo, respuesta = signal.step(sistema)
    
    # Graficar la respuesta
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, respuesta, label='Respuesta al escalón')
    plt.title(f'Respuesta al Escalón (K={K}, ωn={omega_n}, ζ={zeta})')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Respuesta')
    plt.ylim([-0.2, 1.2] if K == 1 else [0, 1.2*K])  # Ajuste de límites basado en K
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Determinar el tipo de sistema
    tipo = tipo_sistema(zeta)
    print(f"Tipo de sistema: {tipo}")

if __name__ == "__main__":
    main()
