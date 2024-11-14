from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306
import board
import busio

# Configuración de la comunicación I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Testeo de la pantalla OLED
def test_oled():
    try:
        RST = None
        disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=0x3C)
        disp.begin()
        disp.clear()
        disp.display()
        
        # Dibujar algo en la pantalla para verificar que funciona
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((0, 0), 'Prueba', font=font, fill=255)
        disp.image(image)
        disp.display()
        print("Pantalla OLED OK")
    except Exception as e:
        print(f"Fallo en la pantalla OLED: {e}")

if __name__ == "__main__":
    test_oled()