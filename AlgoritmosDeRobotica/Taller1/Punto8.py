import random

def generar_numeros_aleatorios(cantidad, minimo, maximo):
    """
    Genera una lista de números aleatorios dentro de un rango específico.

    :param cantidad: Número de números aleatorios a generar.
    :param minimo: Valor mínimo del rango.
    :param maximo: Valor máximo del rango.
    :return: Lista de números aleatorios.
    """
    return [random.uniform(minimo, maximo) for _ in range(cantidad)]

def main():
    # Solicitar datos al usuario
    cantidad = int(input("Ingrese la cantidad de números aleatorios a generar: "))
    minimo = float(input("Ingrese el valor mínimo del rango: "))
    maximo = float(input("Ingrese el valor máximo del rango: "))

    # Generar números aleatorios
    numeros = generar_numeros_aleatorios(cantidad, minimo, maximo)
    
    # Mostrar los números generados
    print(f"Números aleatorios generados:")
    for numero in numeros:
        print(f"{numero:.2f}")

if __name__ == "__main__":
    main()
