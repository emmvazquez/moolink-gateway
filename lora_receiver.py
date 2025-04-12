import time
import spidev
import RPi.GPIO as GPIO
import json
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import *

# 🚀 Configura la Raspberry Pi
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        print("\n📦 ¡Paquete recibido!")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        raw_data = bytes(payload).decode('utf-8', errors='ignore')
        print(f"📝 Contenido crudo: {raw_data}")

        try:
            data_json = json.loads(raw_data)
            print("📖 JSON decodificado:")
            print(json.dumps(data_json, indent=4))
        except json.JSONDecodeError:
            print("⚠️ Error: No se pudo decodificar como JSON.")

        print(f"📶 RSSI: {self.get_rssi_value()} dBm")
        print(f"📈 SNR: {self.get_pkt_snr_value()} dB")

        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

lora = LoRaReceiver(verbose=False)

lora.set_mode(MODE.STDBY)
lora.set_freq(915.0)
lora.set_spreading_factor(7)               # SF7 correcto
lora.set_bw(BW.BW125)                       # 125kHz correcto
lora.set_coding_rate(CODING_RATE.CR4_5)     # CR4/5 correcto
lora.set_preamble(8)
lora.set_rx_crc(True)

print("✅ Receptor LoRa iniciado en Raspberry Pi...")
time.sleep(1)

lora.set_mode(MODE.RXCONT)
print("🎯 Modo RXCONT activo. Esperando paquetes...\n")

try:
    while True:
        irq_flags = lora.get_irq_flags()
        if irq_flags.get('rx_done'):
            lora.on_rx_done()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n⛔ Interrumpido por usuario.")
finally:
    BOARD.teardown()
