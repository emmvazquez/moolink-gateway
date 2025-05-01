import time
import json
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE

class MooLinkReceiver(LoRa):
    def __init__(self, verbose=False):
        super(MooLinkReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        raw = bytes(payload).decode('utf-8', errors='ignore')

        print("\n Paquete recibido:")
        print(f" Datos crudos: {raw}")

        try:
            data = json.loads(raw)
            print(" JSON decodificado:")
            for k, v in data.items():
                print(f"  {k}: {v}")
        except Exception as e:
            print(f"Error decodificando JSON: {e}")

        print(f" RSSI: {self.get_rssi_value()} dBm")
        print(f" SNR: {self.get_pkt_snr_value()} dB")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

# --- Configurar el board y la radio ---
BOARD.setup()
lora = MooLinkReceiver(verbose=False)

# === Parámetros iguales al emisor ESP32-S3 ===
lora.set_freq(915.0)  # MHz
lora.set_spreading_factor(12)
lora.set_bw(BW.BW125)  # 125 kHz
lora.set_coding_rate(CODING_RATE.CR4_8)  # 4/8
lora.set_preamble(8)
lora.set_rx_crc(True)
lora.set_sync_word(0x34)

# --- Iniciar recepción ---
lora.reset_ptr_rx()
lora.set_mode(MODE.RXCONT)

print("📡 Receptor MooLink iniciado. Esperando paquetes...")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n Interrumpido por el usuario.")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
