"""
Proyecto: MooLink - Receptor LoRa RAW (Raspberry Pi)
Fecha: 12 de mayo de 2025
Versión: 4.0.2
Descripción:
Receptor en Raspberry Pi con SX1278 usando lectura por
polling. Decodifica mensajes delimitados tipo @...#
enviados desde ESP32-S3 con SX1262.
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time

# Desactivar configuración de pines que causa conflictos
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

# Configurar receptor
lora = LoRaReceiver(verbose=False)
lora.set_freq(915.0)
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor LoRa listo. Esperando mensajes...\n")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = bytes(lora.read_payload(nocheck=True))
            print("📦 RAW:", payload)

            if payload.startswith(b'@') and payload.endswith(b'#'):
                mensaje = payload[1:-1].decode('utf-8', errors='ignore')
                print("✅ Mensaje recibido:", mensaje)
            else:
                print("⚠️ Formato no válido")

        time.sleep(0.1)

except KeyboardInterrupt:
    lora.set_mode(MODE.SLEEP)
    print("\n⛔ Interrumpido manualmente.")
