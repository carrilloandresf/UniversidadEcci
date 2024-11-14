import board
import busio
import adafruit_ahtx0
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306

# Configuración de la comunicación I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Escaneo de dispositivos I2C
def scan_i2c_devices():
    while not i2c.try_lock():
        pass
    try:
        devices = i2c.scan()
        if devices:
            print("Dispositivos I2C encontrados:")
            for device in devices:
                print(f"Dirección: {hex(device)}")
        else:
            print("No se encontraron dispositivos I2C.")
    finally:
        i2c.unlock()

# Intentar identificar el sensor de humedad y la pantalla OLED
def identify_devices():
    while not i2c.try_lock():
        pass
    try:
        devices = i2c.scan()
        for address in devices:
            try:
                # Intentar inicializar el sensor de humedad AHTx0
                sensor = adafruit_ahtx0.AHTx0(i2c, address=address)
                temperature = sensor.temperature
                humidity = sensor.relative_humidity
                print(f"Sensor de humedad encontrado en dirección {hex(address)} - Temperatura: {temperature:.2f} °C, Humedad: {humidity:.2f} %")
                print(f"Para usar el sensor de humedad en el código: sensor = adafruit_ahtx0.AHTx0(i2c, address={hex(address)})")
                continue
            except Exception as e:
                pass

            try:
                # Intentar inicializar la pantalla OLED
                RST = None
                disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address=address)
                disp.begin()
                disp.clear()
                disp.display()
                width = disp.width
                height = disp.height
                image = Image.new('1', (width, height))
                draw = ImageDraw.Draw(image)
                font = ImageFont.load_default()
                draw.text((0, 0), 'Prueba OLED', font=font, fill=255)
                disp.image(image)
                disp.display()
                print(f"Pantalla OLED encontrada en dirección {hex(address)}")
                print(f"Para usar la pantalla OLED en el código: disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_address={hex(address)})")
            except Exception as e:
                pass
    finally:
        i2c.unlock()

if __name__ == "__main__":
    print("Escaneando dispositivos I2C...")
    scan_i2c_devices()
    print("\nIntentando identificar dispositivos conectados...")
    identify_devices()