import matplotlib.pyplot as plt

def dibujar_nombre(nombre):
    # Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(15, 6))

    # Definir los datos para cada letra
    letras = {
        'F': [(0, 0), (0, 4), None, (0, 4), (2, 4), None, (0, 2), (1.5, 2)],
        'E': [(0, 0), (0, 4), None, (0, 4), (2, 4), None, (0, 2), (1.5, 2), None, (0, 0), (2, 0)],
        'L': [(0, 4), (0, 0), None, (0, 0), (2, 0)],
        'I': [(1, 0), (1, 4)],
        'P': [(0, 0), (0, 4), None, (0, 4), (2, 4), (2, 2), (0, 2)],
        'D': [(0, 0), (0, 4), None, (0, 4), (2, 3), (2, 1), (0, 0)],
        'A': [(0, 0), (1, 4), (2, 0), None, (0.5, 2), (1.5, 2)],
        'N': [(0, 0), (0, 4), None, (0, 4), (2, 0), None, (2, 0), (2, 4)],
        'O': [(0, 0), (0, 4), (2, 4), (2, 0), (0, 0)],
        'J': [(2, 4), (2, 1), (0, 0)],
        'S': [(2, 4), (0, 4), (0, 2), (2, 2), (2, 0), (0, 0)],
        'W': [(0, 4), (0.5, 0), (1, 4), (1.5, 0), (2, 4)],
        'M': [(0, 0), (0, 4), (1, 2), (2, 4), (2, 0)],
        ' ': []  # Espacio en blanco
    }

    # Espaciado entre letras
    espaciado = 6  # Aumentado para mayor separación

    # Posición inicial
    x_offset = 0

    # Dibujar el nombre seleccionado
    for letra in nombre.upper():
        if letra in letras:
            coords = letras[letra]
            for i in range(len(coords)):
                if coords[i] is None:
                    continue
                x = [coords[i][0] + x_offset, coords[i + 1][0] + x_offset] if i + 1 < len(coords) and coords[i + 1] is not None else None
                y = [coords[i][1], coords[i + 1][1]] if i + 1 < len(coords) and coords[i + 1] is not None else None
                if x and y:
                    ax.plot(x, y, marker='o', color='blue')
            x_offset += espaciado

    # Configurar los límites y el título
    ax.set_xlim(-2, x_offset)
    ax.set_ylim(-1, 5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Nombre proyectado: {nombre}')

    # Mostrar el gráfico
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    nombres = ["Felipe", "Daniela", "Jeisson", "William"]
    
    while True:
        # Mostrar los nombres disponibles
        print("Seleccione un nombre para proyectar:")
        for i, nombre in enumerate(nombres):
            print(f"{i + 1}. {nombre}")
        
        # Solicitar la selección del usuario
        seleccion = input("Ingrese el número correspondiente al nombre (o 'q' para salir): ")
        
        if seleccion.lower() == 'q':
            print("Saliendo del programa.")
            break

        # Validar la selección
        if seleccion.isdigit():
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(nombres):
                nombre_seleccionado = nombres[seleccion - 1]
                dibujar_nombre(nombre_seleccionado)
            else:
                print("Selección inválida. Por favor, intente de nuevo.")
        else:
            print("Entrada no válida. Por favor, ingrese un número.")
