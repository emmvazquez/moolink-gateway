import time
import spidev
import RPi.GPIO as GPIO
import json
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import *

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

        # Intentamos interpretar como JSON
        try:
            data_json = json.loads(raw_data)
            print("📖 JSON decodificado:")
            print(json.dumps(data_json, indent=4))
        except json.JSONDecodeError:
            print("⚠️ Error: No se pudo decodificar como JSON.")

        print(f"📶 RSSI: {self.get_rssi_value()} dBm")
        print(f"📈 SNR: {self.get_pkt_snr_value()} dB")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

lora = LoRaReceiver(verbose=False)

# Configuraciones igual que el emisor
lora.set_mode(MODE.STDBY)
lora.set_freq(915.0)
lora.set_spreading_factor(7)
lora.set_bandwidth(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_crc(True)
lora.set_iq_inversion(False)

lora.set_rx_crc(True)

print("✅ Receptor LoRa iniciado en Raspberry Pi...")
time.sleep(1)

try:
    lora.start()
except KeyboardInterrupt:
    print("⛔ Interrumpido por usuario.")
finally:
    BOARD.teardown()
