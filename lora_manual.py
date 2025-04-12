# === MooLink - Receptor Manual Raspberry Pi + SX1278 ===

import time
import spidev
import RPi.GPIO as GPIO

# === Pines conectados ===
CS_PIN = 8      # CE0
RESET_PIN = 25  # Reset LoRa
DIO0_PIN = 4    # DIO0 para interrupciones

# === Inicializar SPI ===
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, dispositivo 0 (CE0)
spi.max_speed_hz = 5000000

# === Inicializar GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)
GPIO.setup(DIO0_PIN, GPIO.IN)

# === Funciones utilitarias ===
def reset_lora():
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)

def write_register(address, value):
    spi.xfer2([address | 0x80, value])

def read_register(address):
    return spi.xfer2([address & 0x7F, 0])[1]

def set_frequency(freq_mhz):
    frf = int((freq_mhz * 1000000.0) / 61.03515625)
    write_register(0x06, (frf >> 16) & 0xFF)
    write_register(0x07, (frf >> 8) & 0xFF)
    write_register(0x08, frf & 0xFF)

def receive_payload():
    irq_flags = read_register(0x12)
    if irq_flags & 0x40:  # RX Done
        write_register(0x12, 0xFF)  # Clear IRQ flags

        current_addr = read_register(0x10)
        received_count = read_register(0x13)

        write_register(0x0D, current_addr)

        payload = []
        for _ in range(received_count):
            payload.append(read_register(0x00))

        rssi = read_register(0x1A) - 137
        snr = (read_register(0x19) & 0xFF) / 4.0

        try:
            text = bytes(payload).decode('utf-8', errors='replace')
            print(f"\n📦 Paquete recibido:")
            print(f"📝 Datos: {text}")
            print(f"📶 RSSI: {rssi} dBm")
            print(f"📈 SNR: {snr} dB")
        except Exception as e:
            print(f"⚠️ Error al decodificar: {e}")

# === Inicio del programa ===
print("🔌 Reseteando LoRa...")
reset_lora()

print("⚙️ Configurando LoRa...")
write_register(0x01, 0x80)  # Sleep + LoRa
set_frequency(915.0)

write_register(0x1D, 0x72)  # BW = 125kHz, Coding Rate 4/8
write_register(0x1E, (12 << 4) | 0x04)  # Spreading Factor 12, CRC ON
write_register(0x26, 0x04)  # LowDataRateOptimize ON
write_register(0x39, 0x34)  # SyncWord = 0x34
write_register(0x33, 0x27)  # No invert IQ

write_register(0x0D, 0x00)  # FIFO RX base address = 0
write_register(0x0E, 0x00)  # FIFO TX base address = 0

write_register(0x01, 0x85)  # LoRa + Standby
write_register(0x40, 0x00)  # DIO0 = RxDone
write_register(0x01, 0x85)  # Standby

print("⏰ Activando receptor continuo...")
write_register(0x01, 0x8D)  # Receive Continuous

print("\n📡 Receptor RAW iniciado. Esperando paquetes...")

try:
    while True:
        if GPIO.input(DIO0_PIN) == GPIO.HIGH:
            receive_payload()
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n❌ Interrumpido por usuario.")

finally:
    write_register(0x01, 0x81)  # Sleep
    spi.close()
    GPIO.cleanup()
    print("🔌 SPI y GPIO liberados.")