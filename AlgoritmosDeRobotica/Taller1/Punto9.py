import math

def volumen_prisma(base_area, altura):
    """
    Calcula el volumen de un prisma.

    :param base_area: Área de la base del prisma.
    :param altura: Altura del prisma.
    :return: Volumen del prisma.
    """
    return base_area * altura

def volumen_piramide(base_area, altura):
    """
    Calcula el volumen de una pirámide.

    :param base_area: Área de la base de la pirámide.
    :param altura: Altura de la pirámide.
    :return: Volumen de la pirámide.
    """
    return (base_area * altura) / 3

def volumen_cono_truncado(radio_menor, radio_mayor, altura):
    """
    Calcula el volumen de un cono truncado.

    :param radio_menor: Radio de la base menor del cono truncado.
    :param radio_mayor: Radio de la base mayor del cono truncado.
    :param altura: Altura del cono truncado.
    :return: Volumen del cono truncado.
    """
    return (math.pi * altura / 3) * (radio_menor**2 + radio_mayor**2 + radio_menor * radio_mayor)

def volumen_cilindro(radio, altura):
    """
    Calcula el volumen de un cilindro.

    :param radio: Radio de la base del cilindro.
    :param altura: Altura del cilindro.
    :return: Volumen del cilindro.
    """
    return math.pi * radio**2 * altura

def main():
    print("Seleccione el sólido para calcular el volumen:")
    print("1. Prisma")
    print("2. Pirámide")
    print("3. Cono truncado")
    print("4. Cilindro")
    
    seleccion = int(input("Ingrese el número del sólido: "))

    if seleccion == 1:
        base_area = float(input("Ingrese el área de la base del prisma: "))
        altura = float(input("Ingrese la altura del prisma: "))
        volumen = volumen_prisma(base_area, altura)
        print(f"El volumen del prisma es {volumen:.2f} unidades cúbicas")

    elif seleccion == 2:
        base_area = float(input("Ingrese el área de la base de la pirámide: "))
        altura = float(input("Ingrese la altura de la pirámide: "))
        volumen = volumen_piramide(base_area, altura)
        print(f"El volumen de la pirámide es {volumen:.2f} unidades cúbicas")

    elif seleccion == 3:
        radio_menor = float(input("Ingrese el radio de la base menor del cono truncado: "))
        radio_mayor = float(input("Ingrese el radio de la base mayor del cono truncado: "))
        altura = float(input("Ingrese la altura del cono truncado: "))
        volumen = volumen_cono_truncado(radio_menor, radio_mayor, altura)
        print(f"El volumen del cono truncado es {volumen:.2f} unidades cúbicas")

    elif seleccion == 4:
        radio = float(input("Ingrese el radio de la base del cilindro: "))
        altura = float(input("Ingrese la altura del cilindro: "))
        volumen = volumen_cilindro(radio, altura)
        print(f"El volumen del cilindro es {volumen:.2f} unidades cúbicas")

    else:
        print("Selección inválida")

if __name__ == "__main__":
    main()
