from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE, SF
import time

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

BOARD.setup()
lora = LoRaReceiver(verbose=False)

# Configuración LoRa compatible con tu emisor
lora.set_freq(915.0)
lora.set_spreading_factor(SF.SF12)
lora.set_bandwidth(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_preamble(8)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

lora.set_mode(MODE.RXCONT)
print("📡 Receptor SX1276 en modo RXCONT sin interrupciones...")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = lora.read_payload(nocheck=True)
            mensaje = bytes(payload).decode('utf-8', errors='ignore')
            print("📥 Paquete recibido:", mensaje)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("⛔ Interrumpido por el usuario.")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
