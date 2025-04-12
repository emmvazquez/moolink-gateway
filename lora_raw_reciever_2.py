import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import *

# Inicializar board
BOARD.setup()

class ForcedLoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(ForcedLoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def force_lora_config(self):
        print("\U0001F50C Forzando configuración LoRa en SX1278...")
        
        self.set_mode(MODE.SLEEP)
        time.sleep(0.1)
        
        # Cambiar a modo LoRa
        self.write_reg(REG.OP_MODE, 0x80)  # LongRangeMode=1 (LoRa), modo sleep
        time.sleep(0.1)

        # Bandwidth: 125kHz (0x70)
        # Coding rate 4/5 (0x02)
        # Explicit header mode (0)
        self.write_reg(REG.LORA.MAC_CONFIG_1, 0x72)  

        # Spreading Factor 7 (SF7)
        # Payload CRC on
        self.write_reg(REG.LORA.MAC_CONFIG_2, 0x74)

        # Sync word (LoRaWAN default 0x34, pero puede ser 0x12)
        self.write_reg(REG.LORA.SYNC_WORD, 0x34)

        # Establecer frecuencia a 915 MHz
        self.set_freq(915.0)

        print("\u2705 Configuración SX1278 forzada correctamente.")

    def read_raw_payload(self):
        payload = self.read_payload(nocheck=True)
        return bytes(payload)

# Instancia
lora = ForcedLoRaReceiver(verbose=False)

# Configurar SX1278 correctamente
lora.force_lora_config()

print("\U0001F50C Cambiando a modo RX continuo...")

try:
    lora.reset_ptr_rx()
    lora.set_mode(MODE.RXCONT)

    while True:
        irq_flags = lora.get_irq_flags()
        if irq_flags['rx_done']:
            print("\n\U0001F4AC Paquete recibido!")
            raw_data = lora.read_raw_payload()
            try:
                text = raw_data.decode('utf-8', errors='replace')
                print(f"\U0001F4DD Datos: {text}")
            except Exception as e:
                print(f"\u26a0\ufe0f Error de decodificación: {e}")
                print(f"Bytes crudos: {raw_data}")

            lora.clear_irq_flags()
            lora.reset_ptr_rx()
            lora.set_mode(MODE.RXCONT)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\u274C Interrumpido por usuario.")
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()