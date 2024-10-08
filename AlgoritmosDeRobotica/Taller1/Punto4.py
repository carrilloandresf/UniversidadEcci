"""
Para calcular la resistencia de una RTD (Detector de Temperatura de Resistencia) de platino PT100 en función de la temperatura, se utiliza la siguiente fórmula:

R(T) = R0 * (1 + α * (T - T0))

donde:

R(T) es la resistencia a la temperatura T.
R0 es la resistencia a la temperatura de referencia T0 (para el PT100, R0 es 100 ohmios a T0 = 0°C).
α es el coeficiente de temperatura del platino (para el PT100, aproximadamente 0.00385 por °C).
T es la temperatura en grados Celsius.
T0 es la temperatura de referencia (0°C).


adicionar
Calculadora RTD
 
Calculadora de resistencia para RTD de platino de conformidad con IEC 60751
Cómo utilizar la calculadora de resistencia RTD:

Introduzca la resistencia RTD a 0°C. (La mayoría de los RTD tienen una resistencia de 100 ohms a 0°C).
Introduzca la temperatura RTD en °C.
Lea la resistencia RTD
 

Calculadora de resistencia para RTD de platino de conformidad con IEC 60751:

 

Introduzca la resistencia RTD a 0°C
Introduzca la temperatura RTD en °C.
Resistencia RTD (ohms)
 

Ecuaciones de Callendar-Van Dusen:


Temperatura RTD ≥ 0°C: Rt = R0(1+At+Bt2)


Temperatura RTD < 0°C: Rt = R0[1+At+Bt2+C(t-100)t3]
"""

def resistencia_pt100(temperatura):
    """
    Calcula la resistencia de una RTD de platino PT100 en función de la temperatura.
    
    :param temperatura: Temperatura en grados Celsius.
    :return: Resistencia en ohmios.
    """
    R0 = 100  # Resistencia a 0°C
    alpha = 0.00385  # Coeficiente de temperatura para PT100
    T0 = 0  # Temperatura de referencia (0°C)
    
    resistencia = R0 * (1 + alpha * (temperatura - T0))
    return resistencia

def main():
    # Solicitar la temperatura al usuario
    temperatura = float(input("Ingrese la temperatura en grados Celsius: "))
    
    # Calcular la resistencia
    resistencia = resistencia_pt100(temperatura)
    
    # Mostrar el resultado
    print(f"La resistencia de la RTD PT100 a {temperatura}°C es {resistencia:.2f} ohmios")

if __name__ == "__main__":
    main()
