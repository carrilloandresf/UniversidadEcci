import board
import busio
import adafruit_ahtx0

# Configuración de la comunicación I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Testeo del sensor de temperatura y humedad
def test_sensor():
    try:
        sensor = adafruit_ahtx0.AHTx0(i2c)
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"Sensor OK - Temperatura: {temperature:.2f} °C, Humedad: {humidity:.2f} %")
    except Exception as e:
        print(f"Fallo en el sensor de temperatura y humedad: {e}")

if __name__ == "__main__":
    test_sensor()