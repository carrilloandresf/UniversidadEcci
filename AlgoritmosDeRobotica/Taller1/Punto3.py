import math

def rectangulares_a_cilindricas(x, y, z):
    """
    Convierte coordenadas rectangulares (x, y, z) a coordenadas cilíndricas (r, theta, z).
    
    :param x: Coordenada x en el sistema rectangular.
    :param y: Coordenada y en el sistema rectangular.
    :param z: Coordenada z en el sistema rectangular.
    :return: Tupla (r, theta, z) en coordenadas cilíndricas.
    """
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta, z

def rectangulares_a_esfericas(x, y, z):
    """
    Convierte coordenadas rectangulares (x, y, z) a coordenadas esféricas (rho, theta, phi).
    
    :param x: Coordenada x en el sistema rectangular.
    :param y: Coordenada y en el sistema rectangular.
    :param z: Coordenada z en el sistema rectangular.
    :return: Tupla (rho, theta, phi) en coordenadas esféricas.
    """
    rho = math.sqrt(x**2 + y**2 + z**2)
    theta = math.atan2(y, x)
    phi = math.acos(z / rho)
    return rho, theta, phi

def main():
    # Coordenadas rectangulares
    x = float(input("Ingrese la coordenada x: "))
    y = float(input("Ingrese la coordenada y: "))
    z = float(input("Ingrese la coordenada z: "))
    
    # Conversión a coordenadas cilíndricas
    r, theta_cilindrico, z_cilindrico = rectangulares_a_cilindricas(x, y, z)
    print(f"Coordenadas cilíndricas:\n r = {r}\n theta = {math.degrees(theta_cilindrico)} grados\n z = {z_cilindrico}")
    
    # Conversión a coordenadas esféricas
    rho, theta_esferico, phi = rectangulares_a_esfericas(x, y, z)
    print(f"Coordenadas esféricas:\n rho = {rho}\n theta = {math.degrees(theta_esferico)} grados\n phi = {math.degrees(phi)} grados")

if __name__ == "__main__":
    main()

"""
Aclaraciones:

Conversión a Coordenadas Cilíndricas:

r: La distancia radial desde el eje z, calculada como sqrt(x^2 + y^2).
theta: El ángulo en el plano xy con respecto al eje x, calculado como atan2(y, x).
z: La coordenada z se mantiene igual.
Conversión a Coordenadas Esféricas:

rho: La distancia desde el origen, calculada como sqrt(x^2 + y^2 + z^2).
theta: El ángulo en el plano xy con respecto al eje x, calculado como atan2(y, x).
phi: El ángulo desde el eje z, calculado como acos(z / rho).
Funciones Trigonométricas:

math.sqrt(): Para calcular la raíz cuadrada.
math.atan2(): Para calcular el ángulo con respecto al eje x.
math.acos(): Para calcular el ángulo con respecto al eje z.
math.degrees(): Para convertir los ángulos de radianes a grados en la salida.
"""