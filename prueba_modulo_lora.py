import spidev
import time

# Configurar el bus SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Dispositivo 0 (CE0)
spi.max_speed_hz = 5000000  # 5 MHz (puedes bajarlo a 1 MHz si falla)

# Función para leer un registro
def read_register(address):
    resp = spi.xfer2([address & 0x7F, 0x00])  # MSB a 0 para lectura
    return resp[1]

# Función para escribir un registro
def write_register(address, value):
    spi.xfer2([address | 0x80, value])  # MSB a 1 para escritura

print("🔍 Probando comunicación con LoRa SX1278...")

# Intento leer el registro de versión
version = read_register(0x42)

print(f"📋 Versión de chip detectada: 0x{version:02X}")

if version == 0x12:
    print("✅ Comunicación SPI OK: SX1276/77/78 detectado.")
else:
    print("⚠️ Error: No se detectó el chip esperado. Revisa conexiones o alimentación.")

spi.close()
