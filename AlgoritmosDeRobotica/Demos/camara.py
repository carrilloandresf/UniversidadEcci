import cv2

# Inicializa la cámara
cam = cv2.VideoCapture(0)  # 0 representa la primera cámara conectada

# Verifica si la cámara está disponible
if not cam.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Captura una foto
ret, frame = cam.read()

if ret:
    # Guarda la foto como 'foto.jpg'
    cv2.imwrite("foto.jpg", frame)
    print("Foto tomada y guardada como 'foto.jpg'")
else:
    print("Error: No se pudo capturar la imagen.")

# Libera la cámara
cam.release()