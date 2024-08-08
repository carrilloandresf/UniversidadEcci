import numpy as np

def rotacion_x(angulo):
    """
    Devuelve la matriz de rotación para una rotación alrededor del eje X.

    :param angulo: Ángulo de rotación en grados.
    :return: Matriz de rotación 3x3 alrededor del eje X.
    """
    radianes = np.radians(angulo)
    matriz = np.array([
        [1, 0, 0],
        [0, np.cos(radianes), -np.sin(radianes)],
        [0, np.sin(radianes), np.cos(radianes)]
    ])
    return matriz

def rotacion_y(angulo):
    """
    Devuelve la matriz de rotación para una rotación alrededor del eje Y.

    :param angulo: Ángulo de rotación en grados.
    :return: Matriz de rotación 3x3 alrededor del eje Y.
    """
    radianes = np.radians(angulo)
    matriz = np.array([
        [np.cos(radianes), 0, np.sin(radianes)],
        [0, 1, 0],
        [-np.sin(radianes), 0, np.cos(radianes)]
    ])
    return matriz

def rotacion_z(angulo):
    """
    Devuelve la matriz de rotación para una rotación alrededor del eje Z.

    :param angulo: Ángulo de rotación en grados.
    :return: Matriz de rotación 3x3 alrededor del eje Z.
    """
    radianes = np.radians(angulo)
    matriz = np.array([
        [np.cos(radianes), -np.sin(radianes), 0],
        [np.sin(radianes), np.cos(radianes), 0],
        [0, 0, 1]
    ])
    return matriz

def main():
    angulo_x = float(input("Ingrese el ángulo de rotación alrededor del eje X (en grados): "))
    angulo_y = float(input("Ingrese el ángulo de rotación alrededor del eje Y (en grados): "))
    angulo_z = float(input("Ingrese el ángulo de rotación alrededor del eje Z (en grados): "))

    matriz_x = rotacion_x(angulo_x)
    matriz_y = rotacion_y(angulo_y)
    matriz_z = rotacion_z(angulo_z)

    print(f"Matriz de rotación alrededor del eje X:\n{matriz_x}")
    print(f"Matriz de rotación alrededor del eje Y:\n{matriz_y}")
    print(f"Matriz de rotación alrededor del eje Z:\n{matriz_z}")

if __name__ == "__main__":
    main()
