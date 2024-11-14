import board
import busio
import adafruit_ahtx0
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306

# Configuración de la comunicación I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Testeo del sensor de temperatura y humedad
def test_sensor():
    try:
        sensor = adafruit_ahtx0.AHTx0(i2c)
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"Sensor OK - Temperatura: {temperature:.2f} °C, Humedad: {humidity:.2f} %")
        return True
    except Exception as e:
        print(f"Fallo en el sensor de temperatura y humedad: {e}")
        return False

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
        draw.text((0, 0), 'Test OLED OK', font=font, fill=255)
        disp.image(image)
        disp.display()
        print("Pantalla OLED OK")
        return True
    except Exception as e:
        print(f"Fallo en la pantalla OLED: {e}")
        return False

# Función principal para testear ambos componentes
def main():
    sensor_ok = test_sensor()
    oled_ok = test_oled()

    if sensor_ok and oled_ok:
        print("Todos los componentes funcionan correctamente.")
    elif not sensor_ok and not oled_ok:
        print("Ambos componentes fallaron. Verifica las conexiones y el estado de los dispositivos.")
    elif not sensor_ok:
        print("El sensor de temperatura y humedad está fallando.")
    elif not oled_ok:
        print("La pantalla OLED está fallando.")

if __name__ == "__main__":
    main()