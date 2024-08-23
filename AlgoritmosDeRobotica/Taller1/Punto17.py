import cv2
import numpy as np

def obtener_contornos(imagen_path):
    # Leer la imagen en color
    imagen = cv2.imread(imagen_path)

    # Convertir la imagen a escala de grises
    imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque gaussiano para reducir el ruido
    imagen_blur = cv2.GaussianBlur(imagen_gray, (5, 5), 0)

    # Aplicar umbral adaptativo para binarizar la imagen
    imagen_binaria = cv2.adaptiveThreshold(imagen_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)

    # Encontrar contornos en la imagen binaria
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contornos

def imprimir_coordenadas(contornos, titulo_imagen):
    print(f"Coordenadas de los contornos en {titulo_imagen}:")
    for i, contorno in enumerate(contornos):
        print(f"  Contorno {i + 1}:")
        for punto in contorno:
            x, y = punto[0]
            print(f"    (x, y) = ({x}, {y})")

def dibujar_contornos(imagen, contornos, color, nombre_ventana):
    # Crear una copia de la imagen original para dibujar los contornos
    imagen_contorno = imagen.copy()

    # Dibujar todos los contornos en la imagen
    cv2.drawContours(imagen_contorno, contornos, -1, color, 2)

    # Mostrar la imagen con contornos en una ventana
    cv2.imshow(nombre_ventana, imagen_contorno)

def centrar_ventana(nombre_ventana):
    # Obtener las dimensiones de la ventana
    ventana_info = cv2.getWindowImageRect(nombre_ventana)
    ventana_ancho, ventana_alto = ventana_info[2], ventana_info[3]

    # Obtener las dimensiones de la pantalla
    screen_res = 1280, 720  # Resolución de pantalla (ajustar según tu monitor)
    x = (screen_res[0] - ventana_ancho) // 2
    y = (screen_res[1] - ventana_alto) // 2

    # Mover la ventana a la posición calculada
    cv2.moveWindow(nombre_ventana, x, y)

def main():
    # Rutas de las imágenes de los logos
    imagen_logo1_path = '../../src/img/Hyundai logo.png'  # Ruta a la imagen del primer logo
    imagen_logo2_path = '../../src/img/Suzuki logo.png'  # Ruta a la imagen del segundo logo

    # Leer las imágenes originales
    imagen_logo1 = cv2.imread(imagen_logo1_path)
    imagen_logo2 = cv2.imread(imagen_logo2_path)

    # Obtener contornos de los logos
    contornos_logo1 = obtener_contornos(imagen_logo1_path)
    contornos_logo2 = obtener_contornos(imagen_logo2_path)

    # Imprimir las coordenadas de los puntos de los contornos
    imprimir_coordenadas(contornos_logo1, "Hyundai Logo")
    imprimir_coordenadas(contornos_logo2, "Suzuki Logo")

    # Mostrar las imágenes originales en ventanas separadas
    cv2.imshow('Imagen Logo 1 Original', imagen_logo1)
    cv2.imshow('Imagen Logo 2 Original', imagen_logo2)

    # Dibujar los contornos en las imágenes
    dibujar_contornos(imagen_logo1, contornos_logo1, (0, 0, 255), 'Logo 1 con Contornos')  # Rojo
    dibujar_contornos(imagen_logo2, contornos_logo2, (0, 255, 0), 'Logo 2 con Contornos')  # Verde

    # Centrar las ventanas en la pantalla
    centrar_ventana('Imagen Logo 1 Original')
    centrar_ventana('Imagen Logo 2 Original')
    centrar_ventana('Logo 1 con Contornos')
    centrar_ventana('Logo 2 con Contornos')

    # Esperar hasta que se presione una tecla
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
