import re
import numpy as np

def txt_to_dict(file_path):
    """
    Lee un archivo txt con coordenadas en el formato (np.int32(x), np.int32(y))
    y las convierte a un diccionario en Python escalado a un rango definido.
    :param file_path: Ruta al archivo txt con las coordenadas.
    :return: Diccionario con las coordenadas en el formato deseado.
    """
    coordinates = []
    pattern = re.compile(r'np\.int32\((\d+)\),\s*np\.int32\((\d+)\)')
    
    # Variables para determinar el rango máximo y mínimo
    min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
    
    # Leer las coordenadas y calcular los valores mínimos y máximos
    with open(file_path, 'r') as file:
        raw_coordinates = []
        for line in file:
            match = pattern.search(line.strip())
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                raw_coordinates.append((x, y))
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)

    # Escalado de las coordenadas al rango [0, 1]
    for x, y in raw_coordinates:
        scaled_x = (x - min_x) / (max_x - min_x) if max_x != min_x else 0.5
        scaled_y = (y - min_y) / (max_y - min_y) if max_y != min_y else 0.5
        coordinates.append((scaled_x, scaled_y))

    return {'Puma': coordinates}

# Ejemplo de uso
file_path = 'C:/Users/anfel/Downloads/contour_coords.txt'
result = txt_to_dict(file_path)
print(result)

# Guardar el resultado como un archivo
output_file_path = 'output_dict.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(str(result))
