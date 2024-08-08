import numpy as np

# Matrices previamente inicializadas
matriz1 = np.array([[1, 2], [3, 4]])
matriz2 = np.array([[5, 6], [7, 8]])

# Suma de matrices
suma = matriz1 + matriz2
print(f"Suma:\n{suma}")

# Resta de matrices
resta = matriz1 - matriz2
print(f"Resta:\n{resta}")

# Producto punto de matrices (multiplicación de matrices)
producto_punto = np.dot(matriz1, matriz2)
print(f"Producto punto:\n{producto_punto}")

# División de matrices (elemento a elemento)
# Manejo de división por cero
try:
    division = np.divide(matriz1, matriz2)
except ZeroDivisionError as e:
    division = "Error: División por cero"
print(f"División:\n{division}")
