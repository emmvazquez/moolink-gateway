import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import *

BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

lora = LoRaReceiver(verbose=False)

lora.set_mode(MODE.STDBY)
lora.set_freq(915.0)
lora.set_spreading_factor(8)               # SF7
lora.set_bw(BW.BW125)                       # 125kHz
lora.set_coding_rate(CODING_RATE.CR4_5)     # CR4/5
lora.set_preamble(8)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("🎯 Escuchando flags LoRa cada segundo...")

try:
    while True:
        flags = lora.get_irq_flags()
        print(f"Flags IRQ: {flags}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n⛔ Interrumpido por usuario.")
finally:
    BOARD.teardown()
