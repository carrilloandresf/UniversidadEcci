import matplotlib.pyplot as plt
import numpy as np

def dibujar_nombre():
    # Crear una figura y un eje
    fig, ax = plt.subplots(figsize=(15, 6))

    # Definir los datos para cada letra
    letras = {
        'F': [(-1, 1), (0, 1), (0, 0), (-1, 0), (0, 0)],
        'E': [(-1, 1), (0, 1), (0, 0), (-1, 0), (0, 0), (-1, 0), (-1, 0)],
        'L': [(0, 1), (0, 0), (1, 0)],
        'I': [(0, 1), (0, 0)],
        'P': [(-1, 1), (0, 1), (0, 0), (-1, 0), (0, 0), (0, 0)],
        'D': [(-1, 1), (0, 1), (0, 0), (-1, 0), (-1, 0), (-1, 0)],
        'A': [(-1, 0), (0, 2), (1, 0), (0, 1)],
        'N': [(-1, 0), (-1, 2), (0, 0), (0, 2)],
        'O': [(-1, 1), (0, 1), (0, 0), (-1, 0), (-1, 1)],
        'J': [(-1, 1), (-1, 0), (-0.5, 0), (0, 0)],
        'S': [(0, 1), (-1, 1), (-1, 0), (0, 0), (0, 1)],
        ' ': []  # Espacio en blanco
    }

    # Espaciado entre letras y nombres
    espaciado = 2
    espaciado_nombre = 10

    # Lista de nombres
    nombres = ["Felipe", "Daniela", "Jeisson"]

    # Posición inicial
    x_offset = 0

    # Dibujar cada nombre
    for nombre in nombres:
        for letra in nombre:
            if letra in letras:
                coords = letras[letra]
                x = [p[0] + x_offset for p in coords]
                y = [p[1] for p in coords]
                ax.plot(x, y, marker='o', label=letra)
                x_offset += 1.5  # Ajustar según sea necesario
        x_offset += espaciado_nombre

    # Configurar los límites y el título
    ax.set_xlim(-2, x_offset)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Nombres en Gráfico 2D')

    # Eliminar la leyenda si es necesario
    ax.legend().set_visible(False)
    
    # Mostrar el gráfico
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    dibujar_nombre()
