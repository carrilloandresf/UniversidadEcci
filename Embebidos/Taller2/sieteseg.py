import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

LEDA = 11
LEDB = 13
LEDC = 15
LEDD = 29
LEDE = 31
LEDF = 37
LEDG = 36

GPIO.setup(LEDA, GPIO.OUT)
GPIO.setup(LEDB, GPIO.OUT)
GPIO.setup(LEDC, GPIO.OUT)
GPIO.setup(LEDD, GPIO.OUT)
GPIO.setup(LEDE, GPIO.OUT)
GPIO.setup(LEDF, GPIO.OUT)
GPIO.setup(LEDG, GPIO.OUT)

print("Iniciando programa...")
sleep(1)

try:
   while True:
      print("Ciclo")
      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.LOW)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.HIGH)
      sleep(1)

      GPIO.output(LEDA, GPIO.HIGH)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.HIGH)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.HIGH)
      GPIO.output(LEDG, GPIO.HIGH)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.HIGH)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.LOW)
      GPIO.output(LEDF, GPIO.HIGH)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.HIGH)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.HIGH)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.HIGH)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.HIGH)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.HIGH)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.LOW)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.HIGH)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.HIGH)
      GPIO.output(LEDG, GPIO.HIGH)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.LOW)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

      GPIO.output(LEDA, GPIO.LOW)
      GPIO.output(LEDB, GPIO.LOW)
      GPIO.output(LEDC, GPIO.LOW)
      GPIO.output(LEDD, GPIO.LOW)
      GPIO.output(LEDE, GPIO.HIGH)
      GPIO.output(LEDF, GPIO.LOW)
      GPIO.output(LEDG, GPIO.LOW)
      sleep(1)

except KeyboardInterrupt:
   GPIO.cleanup()
