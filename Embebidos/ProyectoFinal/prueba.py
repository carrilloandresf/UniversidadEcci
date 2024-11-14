import board
import busio
import adafruit_ahtx0

i2c = busio.I2C(board.SCL, board.SDA)

try:
    sensor = adafruit_ahtx0.AHTx0(i2c)
    print(f"Temperatura: {sensor.temperature} °C")
    print(f"Humedad: {sensor.relative_humidity} %")
except RuntimeError as e:
    print(f"Error de calibración: {e}")
