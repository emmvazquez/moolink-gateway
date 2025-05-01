from SX127x.board_config import BOARD
from SX127x.LoRa import LoRa
from SX127x.constants import MODE, BW, CODING_RATE
import time

# 🔧 Desactivar interrupciones si no se usan
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

# 🔧 Inicializar objeto LoRa y parámetros
lora = LoRaReceiver(verbose=False)
lora.set_freq(915.0)
lora.set_spreading_factor(12)
lora.set_bw(BW.BW125)  # ← aquí era el error anterior
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_preamble(8)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor listo en modo RXCONT...")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = lora.read_payload(nocheck=True)
            raw_bytes = bytes(payload)

            # Validar delimitadores @...#
            if raw_bytes.startswith(b'@') and raw_bytes.endswith(b'#'):
                contenido = raw_bytes[1:-1]  # quitar delimitadores
                try:
                    mensaje = contenido.decode('utf-8')
                    print("✅ Mensaje limpio:", mensaje)

                    partes = mensaje.split(',')
                    if len(partes) == 11:
                        print("📊 CSV parseado:", partes)
                    else:
                        print(f"⚠️ Campos inesperados ({len(partes)}):", partes)

                except UnicodeDecodeError as e:
                    print("❌ Error de codificación UTF-8:", e)
                except Exception as e:
                    print("⚠️ Error general:", e)
            else:
                print("⚠️ Delimitadores ausentes. Ignorado.")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("⛔ Interrupción por teclado")
    lora.set_mode(MODE.SLEEP)
