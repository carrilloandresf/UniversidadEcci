import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)

try:
    pca = PCA9685(i2c)
    pca.deinit()
    print("PCA9685 detected successfully!")
except ValueError as e:
    print(f"Error: {e}")
