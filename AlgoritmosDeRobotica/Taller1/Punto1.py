import numpy as np

# Vectores previamente inicializados
vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 6])

# Suma de vectores
suma = vector1 + vector2
print(f"Suma: {suma}")

# Resta de vectores
resta = vector1 - vector2
print(f"Resta: {resta}")

# Producto punto de vectores
producto_punto = np.dot(vector1, vector2)
print(f"Producto punto: {producto_punto}")

# Producto cruz de vectores
producto_cruz = np.cross(vector1, vector2)
print(f"Producto cruz: {producto_cruz}")

# División de vectores (elemento a elemento)
# Manejo de división por cero
try:
    division = np.divide(vector1, vector2)
except ZeroDivisionError as e:
    division = "Error: División por cero"
print(f"División: {division}")
