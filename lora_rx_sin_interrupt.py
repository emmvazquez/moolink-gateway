from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time

# Anula funciones que no usas (sin interrupciones)
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

# Instancia
lora = LoRaReceiver(verbose=False)
lora.set_freq(915.0)
lora.set_spreading_factor(12)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_preamble(8)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor LoRa (SX1276) listo para recibir...")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = bytes(lora.read_payload(nocheck=True))

            print("📦 Bytes crudos:", list(payload))
            print("📦 Texto crudo:", payload)

            if payload.startswith(b'@') and payload.endswith(b'@'):
                try:
                    msg = payload[1:-1].decode('utf-8')
                    print("✅ Mensaje recibido:", msg)
                except Exception as e:
                    print("⚠️ Error al decodificar:", e)
            else:
                print("⚠️ Delimitadores ausentes. Ignorado.")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("⛔ Interrumpido por usuario")
    lora.set_mode(MODE.SLEEP)
