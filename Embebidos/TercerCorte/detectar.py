import Adafruit_GPIO.Platform as Platform

platform = Platform.platform_detect()
print(f"Plataforma detectada: {platform}")