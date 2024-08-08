"""
Para calcular la potencia consumida en un circuito, se usa la fórmula básica de la potencia eléctrica:

P=V×I

donde:

P es la potencia (en vatios).
V es el voltaje (en voltios).
I es la corriente (en amperios).
"""
def calcular_potencia(voltage, corriente):
    """
    Calcula la potencia consumida en un circuito eléctrico.
    
    :param voltage: Voltaje en voltios.
    :param corriente: Corriente en amperios.
    :return: Potencia en vatios.
    """
    return voltage * corriente

def main():
    # Solicitar datos al usuario
    voltaje = float(input("Ingrese el voltaje en voltios: "))
    corriente = float(input("Ingrese la corriente en amperios: "))
    
    # Calcular la potencia
    potencia = calcular_potencia(voltaje, corriente)
    
    # Mostrar el resultado
    print(f"La potencia consumida en el circuito es {potencia:.2f} vatios")

if __name__ == "__main__":
    main()
