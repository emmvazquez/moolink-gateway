import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE

# Inicializar SPI y pines
BOARD.setup()

class LoRaRSSI(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRSSI, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

# Crear objeto LoRa
lora = LoRaRSSI(verbose=False)

# Configuración LoRa igual al emisor
lora.set_mode(MODE.STDBY)
lora.set_freq(915.0)                   # ✅ Frecuencia 915 MHz
lora.set_spreading_factor(12)            # ✅ SF7
lora.set_bw(BW.BW125)                   # ✅ 125kHz
lora.set_coding_rate(CODING_RATE.CR4_8) # ✅ CR 4/5
lora.set_preamble(8)                    # ✅ Preamble length 8
lora.set_rx_crc(True)                   # ✅ CRC activado

# Ponemos en modo de recibir continuamente
lora.set_mode(MODE.RXCONT)

print("📡 Leyendo RSSI continuamente... (presiona CTRL+C para salir)")

try:
    while True:
        rssi = lora.get_rssi_value()
        print(f"RSSI: {rssi} dBm")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("⛔ Interrumpido por usuario.")
finally:
    BOARD.teardown()
