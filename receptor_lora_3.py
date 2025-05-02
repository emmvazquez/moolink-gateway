from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE
import time

# 🔒 Desactiva interrupciones y configura la placa
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoraTester(LoRa):
    def __init__(self, verbose=False):
        super(LoraTester, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

lora = LoraTester(verbose=False)

# 🧩 Leer registro de versión del chip
version_reg = lora.get_register(0x42)
print(f"🧪 Versión SX127x: 0x{version_reg:02X}")

# ✅ Configuración básica para poner el chip en modo recepción
lora.set_freq(915.0)
lora.set_spreading_factor(7)
lora.set_bw(LoRa.BW.BW125)
lora.set_coding_rate(LoRa.CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)

lora.set_mode(MODE.RXCONT)
print("📡 Modo RXCONT activo... Esperando paquetes...\n")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = bytes(lora.read_payload(nocheck=True))
            print("📦 Paquete recibido:", payload)

            # Diagnóstico: RSSI y SNR
            raw_rssi = lora.get_register(0x1A)
            raw_snr  = lora.get_register(0x19)
            rssi = -164 + raw_rssi
            snr = (raw_snr if raw_snr < 128 else raw_snr - 256) / 4.0

            print(f"📶 RSSI: {rssi} dBm | SNR: {snr:.1f} dB\n")

        time.sleep(0.05)

except KeyboardInterrupt:
    lora.set_mode(MODE.SLEEP)
    print("\n⛔ Interrumpido por usuario.")
