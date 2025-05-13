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

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE
import time

# Configurar pines según el cableado físico
BOARD.setup()
BOARD.reset_pin = 25     # RESET - Blanco
BOARD.ss_pin    = 8      # NSS (CS) - Morado
BOARD.DIO0      = 7      # DIO0 - Naranja

class LoRaReceiver(LoRa):
    def __init__(self):
        super(LoRaReceiver, self).__init__()
        self.set_mode(MODE.SLEEP)

        self.set_freq(915.0)               # Ajustar según la frecuencia usada por el emisor
        self.set_spreading_factor(7)       # SF7
        self.set_bw(7)                     # 125 kHz
        self.set_coding_rate(1)            # 4/5
        self.set_preamble(8)               # 8 símbolos
        self.set_sync_word(0x12)           # Debe coincidir con el emisor
        self.enable_crc()                  # Activar CRC

        self.set_mode(MODE.RXCONT)         # Modo recepción continua

    def on_rx_done(self):
        print("📥 Paquete recibido:")
        payload = bytes(self.read_payload(nocheck=True)).decode('utf-8', errors='ignore')
        print(f"📦 Datos: {payload}")
        print(f"🔊 RSSI: {self.packet_rssi()}, SNR: {self.packet_snr():.2f} dB\n")
        self.set_mode(MODE.RXCONT)

# Instanciar y ejecutar
lora = LoRaReceiver()
lora.set_mode(MODE.RXCONT)

try:
    while True:
        if lora.received_packet:
            lora.on_rx_done()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("⛔ Terminando recepción...")
    BOARD.teardown()
