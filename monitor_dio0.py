import RPi.GPIO as GPIO
import time

# Número de pin GPIO donde está conectado DIO0 (modo BCM)
DIO0_PIN = 25

# Configuración inicial del GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIO0_PIN, GPIO.IN)

print("⏱️ Monitoreando el pin DIO0 (GPIO 25). Presiona CTRL+C para salir.")

try:
    while True:
        level = GPIO.input(DIO0_PIN)
        estado = "🔺 ALTO (1)" if level else "🔻 BAJO (0)"
        print(f"DIO0 nivel: {estado}")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n⛔ Monitoreo detenido por el usuario.")

finally:
    GPIO.cleanup()
