import cv2
import os

# Ruta de la imagen (ajusta esta ruta a la ubicación de tu imagen)
image_path = 'C:/Users/anfel/Downloads/puma_logo.png'

# Cargar la imagen
image = cv2.imread(image_path)

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Invertir los colores para asegurar que el contorno del logo sea blanco sobre fondo negro
inverted_gray = cv2.bitwise_not(gray)

# Aplicar un desenfoque ligero para reducir el ruido
blurred = cv2.GaussianBlur(inverted_gray, (5, 5), 0)

# Aplicar umbral para obtener una imagen binaria (ajusta el valor del umbral si es necesario)
_, threshold = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

# Encontrar los contornos usando cv2.RETR_TREE para obtener todos los contornos
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Extraer las coordenadas de los contornos
contour_coords = []
for contour in contours:
    for point in contour:
        x, y = point[0]
        contour_coords.append((x, y))

# Guardar las coordenadas en un archivo de texto
output_path = os.path.join(os.path.dirname(image_path), 'contour_coords.txt')
with open(output_path, 'w') as file:
    for coord in contour_coords:
        file.write(f"{coord}\n")

print(f"Coordenadas guardadas en: {output_path}")

# Mostrar la imagen y los contornos (opcional)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
cv2.imshow('Contornos', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
