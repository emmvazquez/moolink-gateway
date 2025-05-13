"""
Proyecto: MooLink - Receptor LoRa punto a punto
Fecha: 12 de mayo de 2025
Versión: 4.0
Descripción:
Este script recibe datos LoRa desde un ESP32-S3 (con SX1262 integrado).
El receptor está montado en una Raspberry Pi y usa un módulo SX1278 con las siguientes conexiones:

Cableado SX1278 ↔ Raspberry Pi:
- VCC  → 3.3V       (Rojo)
- GND  → GND        (Negro)
- MOSI → GPIO 10    (Verde)
- MISO → GPIO 9     (Amarillo)
- SCK  → GPIO 11    (Azul)
- NSS  → GPIO 8     (Morado)
- RESET→ GPIO 25    (Blanco)
- DIO0 → GPIO 7     (Naranja)
"""
import RPi.GPIO as GPIO
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE
import time

# Configurar pines según tu cableado
BOARD.setup()
BOARD.reset_pin = 25     # RESET - Blanco
BOARD.ss_pin    = 8      # NSS (CS) - Morado
BOARD.DIO0      = 7      # DIO0 - Naranja

# 🔧 Asegúrate de configurar DIO0 como entrada ANTES de usar interrupciones
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOARD.DIO0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Agrega esta línea
GPIO.setwarnings(False)  # Opcional, para suprimir advertencias

class LoRaReceiver(LoRa):
    def __init__(self):
        super(LoRaReceiver, self).__init__()
        self.set_mode(MODE.SLEEP)

        self.set_freq(915.0)
        self.set_spreading_factor(7)
        self.set_bw(7)
        self.set_coding_rate(1)
        self.set_preamble(8)
        self.set_sync_word(0x12)
        self.enable_crc()

        self.set_mode(MODE.RXCONT)

    def on_rx_done(self):
        print("📥 Paquete recibido:")
        payload = bytes(self.read_payload(nocheck=True)).decode('utf-8', errors='ignore')
        print(f"📦 Datos: {payload}")
        print(f"🔊 RSSI: {self.packet_rssi()}, SNR: {self.packet_snr():.2f} dB\n")
        self.set_mode(MODE.RXCONT)

# Iniciar recepción
lora = LoRaReceiver()
lora.set_mode(MODE.RXCONT)

try:
    while True:
        if lora.received_packet:
            lora.on_rx_done()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("⛔ Terminando...")
    BOARD.teardown()
