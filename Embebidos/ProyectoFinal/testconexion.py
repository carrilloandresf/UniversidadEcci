import board
import busio

# Utilidad para escanear los dispositivos I2C conectados
i2c = busio.I2C(board.SCL, board.SDA)
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