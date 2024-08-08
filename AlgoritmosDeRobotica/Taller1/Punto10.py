def tipo_robot(seleccion):
    """
    Devuelve el tipo y número de articulaciones basado en la selección del usuario.
    
    :param seleccion: Número de selección del usuario.
    :return: Descripción del tipo de robot y el número de articulaciones.
    """
    if seleccion == 1:
        return "Robot Cilíndrico: Tiene 3 articulaciones (dos rotativas y una lineal)."
    elif seleccion == 2:
        return "Robot Cartesiano: Tiene 3 articulaciones lineales (movimientos en X, Y y Z)."
    elif seleccion == 3:
        return "Robot Esférico: Tiene 3 articulaciones (una rotativa y dos esféricas)."
    else:
        return "Selección inválida. Por favor, seleccione un número entre 1 y 3."

def main():
    print("Seleccione el tipo de robot:")
    print("1. Robot Cilíndrico")
    print("2. Robot Cartesiano")
    print("3. Robot Esférico")
    
    seleccion = int(input("Ingrese el número del tipo de robot: "))
    
    # Obtener el tipo y número de articulaciones del robot seleccionado
    resultado = tipo_robot(seleccion)
    
    # Mostrar el resultado
    print(resultado)

if __name__ == "__main__":
    main()
