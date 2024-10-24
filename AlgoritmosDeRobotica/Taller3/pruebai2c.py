import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)

# Lista de direcciones I2C comunes para PCA9685
direcciones = [0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47]

for direccion in direcciones:
    try:
        pca = PCA9685(i2c, address=direccion)
        pca.deinit()
        print(f"PCA9685 detected successfully at address: 0x{direccion:02x}")
        break
    except ValueError as e:
        print(f"No I2C device at address: 0x{direccion:02x}")