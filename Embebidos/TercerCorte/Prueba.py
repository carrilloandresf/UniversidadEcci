import Adafruit_GPIO.Platform as Platform
import Adafruit_GPIO.I2C as I2C

# Configuración de la pantalla OLED y dirección I2C
if Platform.platform_detect() == Platform.RASPBERRY_PI:
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c=I2C.get_i2c_device(0x3C))
else:
    raise RuntimeError("Plataforma no soportada.")
