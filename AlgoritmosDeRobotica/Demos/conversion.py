import re
import numpy as np
import matplotlib.pyplot as plt
import cv2

def txt_to_dict(file_path, image_shape):
    """
    Lee un archivo txt con coordenadas de contorno y las convierte a un diccionario en Python escalado a un rango definido,
    manteniendo la relación de aspecto.
    :param file_path: Ruta al archivo txt con las coordenadas.
    :param image_shape: Tupla con las dimensiones de la imagen (altura, ancho).
    :return: Diccionario con las coordenadas escaladas proporcionalmente y centradas.
    """
    try:
        # Leer el archivo de coordenadas
        print(f"Leyendo coordenadas desde: {file_path}")
        with open(file_path, 'r') as file:
            raw_coordinates = []
            # Ajustar el patrón para que coincida con el formato np.int32(x), np.int32(y)
            pattern = re.compile(r'np\.int32\((\d+)\),\s*np\.int32\((\d+)\)')

            # Leer las coordenadas del archivo
            for line in file:
                match = pattern.search(line.strip())
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                    raw_coordinates.append((x, y))

        # Si no se encontraron coordenadas, devolver un diccionario vacío
        if not raw_coordinates:
            print("No se encontraron coordenadas en el archivo.")
            return {'Puma': []}
        
        # Imprimir las coordenadas originales
        print("\nCoordenadas originales:")
        for coord in raw_coordinates:
            print(f"({coord[0]}, {coord[1]})")

        # Obtener las dimensiones de la imagen
        img_height, img_width = image_shape
        print(f"Dimensiones de la imagen: ancho={img_width}, alto={img_height}")

        # Normalizar las coordenadas al rango [0, 1]
        normalized_coordinates = [
            (
                x / img_width,
                y / img_height
            )
            for x, y in raw_coordinates
        ]

        # Definir los límites para el escalado objetivo (el cuadro objetivo)
        target_min_x, target_max_x = 0.2, 1.0
        target_min_y, target_max_y = 0.2, 1.0

        # Escalar las coordenadas normalizadas al cuadro objetivo
        target_width = target_max_x - target_min_x
        target_height = target_max_y - target_min_y

        scaled_coordinates = [
            (
                target_min_x + coord_x * target_width,
                target_min_y + coord_y * target_height
            )
            for coord_x, coord_y in normalized_coordinates
        ]

        # Imprimir las coordenadas escaladas
        print("\nCoordenadas escaladas:")
        for coord in scaled_coordinates:
            print(f"({coord[0]:.4f}, {coord[1]:.4f})")

        return {'original': raw_coordinates, 'scaled': scaled_coordinates}

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta especificada: {file_path}")
        return {'Puma': []}
    except Exception as e:
        print(f"Error: {e}")
        return {'Puma': []}

# Ruta de la imagen y dimensiones
image_path = 'C:/Users/anfel/Downloads/descarga (1).png'

# Leer la imagen para obtener sus dimensiones
print(f"Leyendo imagen desde: {image_path}")
image = cv2.imread(image_path)

if image is None:
    print(f"Error: No se pudo cargar la imagen desde {image_path}")
else:
    img_height, img_width, _ = image.shape

    # Ruta del archivo de coordenadas
    file_path = 'C:/Users/anfel/Downloads/contour_coords.txt'
    result = txt_to_dict(file_path, (img_height, img_width))

    # Guardar las coordenadas en archivos de texto
    if 'original' in result and 'scaled' in result:
        original_coords = result['original']
        scaled_coords = result['scaled']

        # Guardar coordenadas originales en un archivo
        original_coords_path = 'C:/Users/anfel/Downloads/original_coords_output.txt'
        with open(original_coords_path, 'w') as file:
            for coord in original_coords:
                file.write(f"np.int32({coord[0]}), np.int32({coord[1]})\n")
        print(f"Coordenadas originales guardadas en: {original_coords_path}")

        # Guardar coordenadas escaladas en un archivo
        scaled_coords_path = 'C:/Users/anfel/Downloads/scaled_coords_output.txt'
        with open(scaled_coords_path, 'w') as file:
            for coord in scaled_coords:
                file.write(f"({coord[0]:.4f}, {coord[1]:.4f}),\n")
        print(f"Coordenadas escaladas guardadas en: {scaled_coords_path}")

        # Graficar las coordenadas originales
        if original_coords:
            x_vals_original, y_vals_original = zip(*original_coords)
            plt.figure()
            plt.scatter(x_vals_original, y_vals_original, c='red', marker='o')
            plt.title("Gráfica de Coordenadas Originales")
            plt.xlabel("Eje X (píxeles)")
            plt.ylabel("Eje Y (píxeles)")
            plt.grid(True)

        # Graficar las coordenadas escaladas
        if scaled_coords:
            x_vals_scaled, y_vals_scaled = zip(*scaled_coords)
            plt.figure()
            plt.scatter(x_vals_scaled, y_vals_scaled, c='blue', marker='o')
            plt.title("Gráfica de Coordenadas Escaladas")
            plt.xlabel("Eje X (escalado)")
            plt.ylabel("Eje Y (escalado)")
            plt.grid(True)

        plt.show()