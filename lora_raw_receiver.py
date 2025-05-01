from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time

BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

lora = LoRaReceiver(verbose=False)
lora.set_freq(915.0)
lora.set_spreading_factor(9)  # ✅ SF9 más robusto
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor LoRa v2.9 escuchando...")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = bytes(lora.read_payload(nocheck=True))
            print("📦 Texto:", payload)

            if payload.startswith(b'@') and payload.endswith(b'#'):
                try:
                    contenido = payload[1:-1].decode('utf-8')
                    partes = contenido.split(",")
                    if len(partes) == 3:
                        print(f"✅ Recibido: ID={partes[0]}, Temp={partes[1]}°C, Hum={partes[2]}%")
                    else:
                        print("⚠️ Formato inesperado:", contenido)
                except Exception as e:
                    print("⚠️ Error al decodificar:", e)
            else:
                print("⚠️ Delimitadores ausentes.")

        time.sleep(0.01)  # ✅ revisión más frecuente

except KeyboardInterrupt:
    lora.set_mode(MODE.SLEEP)
    print("⛔ Interrumpido por usuario.")
