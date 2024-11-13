# Inicializamos la cámara
camera = PiCamera()
camera.resolution = (640, 480)  # Puedes ajustar la resolución según lo necesites
camera.framerate = 30
raw_capture = PiRGBArray(camera, size=(640, 480))

# Permitimos que la cámara se inicialice
print("Inicializando la cámara...")
time.sleep(2)  # Espera de 2 segundos para asegurarse de que la cámara está lista

# Capturamos las imágenes de la cámara en un bucle para procesarlas
print("Presiona 'q' para salir, 's' para guardar una imagen")
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    # Convertimos la imagen capturada a un array que pueda usar OpenCV
    image = frame.array

    # Mostramos la imagen en una ventana
    cv2.imshow("Raspberry Pi Camera", image)

    # Aquí puedes realizar el procesamiento con OpenCV que necesites
    # Ejemplo: Convertir a escala de grises y detectar bordes
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 50, 150)
    
    # Mostrar la imagen con bordes detectados
    cv2.imshow("Edges", edges)

    # Presionamos 'q' para salir del bucle o 's' para guardar una imagen
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        # Guardamos la imagen con un nombre específico
        filename = "captura.jpg"
        cv2.imwrite(filename, image)
        print(f"Imagen guardada como {filename}")

    # Limpiamos el stream para la siguiente captura
    raw_capture.truncate(0)

# Cerramos las ventanas de OpenCV
cv2.destroyAllWindows()
