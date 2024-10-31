import Adafruit_GPIO.I2C as I2C
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import time

# Configuración de la pantalla OLED
RST = None  # No se usa el pin de reset, se utiliza None
# Dirección I2C por defecto para la pantalla OLED SSD1306
ADDRESS = 0x3C

# Inicializar la pantalla OLED
oled = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
oled.begin()
oled.clear()
oled.display()

# Crear una imagen en modo 1 (blanco y negro)
width = oled.width
height = oled.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Cargar una fuente (opcional, puedes usar la fuente por defecto)
# font = ImageFont.load_default()  # Fuente por defecto
font = ImageFont.truetype('LiberationSerif-Regular.ttf', 20)  # Asegúrate de que la fuente esté disponible

# Calcular la posición para centrar la letra "e"
text = "E"
(text_width, text_height) = draw.textsize(text, font=font)
x = (width - text_width) // 2
y = (height - text_height) // 2

# Dibujar la letra "e" en el centro
draw.text((x, y), text, font=font, fill=1)
oled.image(image)
oled.display()

# Esperar un momento para que se muestre la letra
time.sleep(3)

# =======================
# Código comentado para imprimir "ECCI"
# =======================
# draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Limpiar la pantalla
# text = "ECCI"
# (text_width, text_height) = draw.textsize(text, font=font)
# x = (width - text_width) // 2
# y = (height - text_height) // 2
# draw.text((x, y), text, font=font, fill=1)
# oled.image(image)
# oled.display()

# Esperar un momento antes de terminar
time.sleep(5)
