"""
Para calcular la fuerza de avance y retroceso de un cilindro neumático de doble efecto, se usa la siguiente fórmula general:

F=P×A

donde:

𝐹
F es la fuerza (en Newtons).
𝑃
P es la presión aplicada (en Pascales).
𝐴
A es el área efectiva del cilindro (en metros cuadrados).
Para un cilindro neumático de doble efecto, las fuerzas de avance y retroceso se calculan considerando el área del vástago en el caso del retroceso.
"""

import math

def calcular_area_cilindro(diametro):
    """
    Calcula el área de la sección transversal del cilindro.
    
    :param diametro: Diámetro del cilindro en metros.
    :return: Área en metros cuadrados.
    """
    radio = diametro / 2
    area = math.pi * radio ** 2
    return area

def calcular_fuerza(presion, area):
    """
    Calcula la fuerza basada en la presión y el área.
    
    :param presion: Presión en Pascales.
    :param area: Área en metros cuadrados.
    :return: Fuerza en Newtons.
    """
    return presion * area

def main():
    # Solicitar datos al usuario
    presion = float(input("Ingrese la presión en Pascales: "))
    diametro = float(input("Ingrese el diámetro del cilindro en metros: "))
    grosor_vastago = float(input("Ingrese el grosor del vástago en metros: "))
    
    # Calcular área de la sección transversal
    area_total = calcular_area_cilindro(diametro)
    area_vastago = calcular_area_cilindro(diametro - 2 * grosor_vastago)
    
    # Calcular fuerzas de avance y retroceso
    fuerza_avance = calcular_fuerza(presion, area_total)
    fuerza_retroceso = calcular_fuerza(presion, area_vastago)
    
    # Mostrar resultados
    print(f"Fuerza de avance: {fuerza_avance:.2f} Newtons")
    print(f"Fuerza de retroceso: {fuerza_retroceso:.2f} Newtons")

if __name__ == "__main__":
    main()
