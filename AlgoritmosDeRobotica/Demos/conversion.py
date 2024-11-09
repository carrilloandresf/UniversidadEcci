import re
import numpy as np

def txt_to_dict(file_path):
    """
    Lee un archivo txt con coordenadas en el formato (np.int32(x), np.int32(y))
    y las convierte a un diccionario en Python escalado a un rango definido.
    :param file_path: Ruta al archivo txt con las coordenadas.
    :return: Diccionario con las coordenadas en el formato deseado.
    """
    try:
        # Leer el archivo
        with open(file_path, 'r') as file:
            raw_coordinates = []
            pattern = re.compile(r'np\.int32\((\d+)\),\s*np\.int32\((\d+)\)')
            
            # Leer las coordenadas usando la expresión regular
            for line in file:
                match = pattern.search(line.strip())
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                    raw_coordinates.append((x, y))

        # Si no se encontraron coordenadas, devolver un diccionario vacío
        if not raw_coordinates:
            return {'Puma': []}
        
        # Determinar los valores mínimos y máximos de x e y
        x_values, y_values = zip(*raw_coordinates)
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        
        # Definir los límites para el escalado
        target_min_x, target_max_x = -0.9, 0.8
        target_min_y, target_max_y = 0.5, 1.2
        
        # Escalar las coordenadas al rango definido por los límites
        coordinates = [
            (
                target_min_x + (x - min_x) / (max_x - min_x) * (target_max_x - target_min_x) if max_x != min_x else (target_min_x + target_max_x) / 2,
                target_min_y + (y - min_y) / (max_y - min_y) * (target_max_y - target_min_y) if max_y != min_y else (target_min_y + target_max_y) / 2
            )
            for x, y in raw_coordinates
        ]
        
        return {'Puma': coordinates}

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo en la ruta especificada: {file_path}")
        return {'Puma': []}
    except Exception as e:
        print(f"Error: {e}")
        return {'Puma': []}

# Ejemplo de uso
file_path = 'C:/Users/anfel/Downloads/contour_coords.txt'
result = txt_to_dict(file_path)
print(result)

# Guardar el resultado como un archivo
output_file_path = 'output_dict.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(str(result))
