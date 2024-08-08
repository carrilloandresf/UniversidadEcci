import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    # Solicitar coordenadas al usuario
    x = float(input("Ingrese la coordenada X del vector: "))
    y = float(input("Ingrese la coordenada Y del vector: "))
    z = float(input("Ingrese la coordenada Z del vector: "))

    # Crear la figura y el eje 3D
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Configurar los límites del gráfico
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])

    # Dibujar el vector
    ax.quiver(0, 0, 0, x, y, z, color='b', arrow_length_ratio=0.1)

    # Etiquetas y título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Vector en Coordenadas 3D')

    # Mostrar la gráfica
    plt.show()

if __name__ == "__main__":
    main()
