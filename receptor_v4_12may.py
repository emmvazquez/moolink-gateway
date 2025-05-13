"""
Proyecto: MooLink - Receptor LoRa punto a punto
Fecha: 12 de mayo de 2025
Versión: 4.0
Descripción: Este script recibe paquetes LoRa desde un ESP32-S3.
Utiliza el módulo SX1278 y la biblioteca SX127x adaptada para Raspberry Pi.
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE
import time

BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self):
        super(LoRaReceiver, self).__init__()
        self.set_mode(MODE.SLEEP)
        self.set_freq(915.0)
        self.set_spreading_factor(7)
        self.set_bw(7)  # 125 kHz
        self.set_coding_rate(1)  # 4/5
        self.set_sync_word(0x12)
        self.set_preamble(8)
        self.enable_crc()
        self.set_mode(MODE.RXCONT)

    def on_rx_done(self):
        print("Mensaje recibido:")
        payload = bytes(self.read_payload(nocheck=True)).decode('utf-8', errors='ignore')
        print(payload)
        self.set_mode(MODE.RXCONT)

lora = LoRaReceiver()
lora.set_mode(MODE.RXCONT)

try:
    while True:
        if lora.received_packet:
            lora.on_rx_done()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Terminando...")
    BOARD.teardown()
