import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import *

# === Inicializar el board y la radio ===
BOARD.setup()

class RawLoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(RawLoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

lora = RawLoRaReceiver(verbose=False)

# Configuración forzada completa
print("\U0001F50C Forzando configuración LoRa en SX1278...")
lora.set_mode(MODE.SLEEP)
time.sleep(0.1)
lora.set_freq(915.0)
lora.set_bw(BW.BW125)
lora.set_spreading_factor(7)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_rx_crc(True)
lora.write_register(0x34)
lora.reset_ptr_rx()
lora.set_mode(MODE.RXCONT)

print("\U0001F4E1 Modo RAW iniciado. Esperando paquetes...")

try:
    while True:
        if lora.get_irq_flags()['rx_done']:
            print("\n\U0001F4AC Paquete detectado!")
            raw_data = lora.read_payload(nocheck=True)
            try:
                text = bytes(raw_data).decode('utf-8', errors='replace')
                print(f"\U0001F4DD Datos recibidos (UTF-8): {text}")
            except Exception as e:
                print(f"\u26a0\ufe0f Error decodificando: {e}")
                print(f"Datos crudos: {raw_data}")

            lora.clear_irq_flags()
            lora.reset_ptr_rx()
            lora.set_mode(MODE.RXCONT)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\u274C Interrumpido por usuario.")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
