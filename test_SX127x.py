from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
import time

# Definir directamente la constante del registro de versión
REG_VERSION = 0x42

class LoraTester(LoRa):
    def __init__(self, verbose=False):
        super(LoraTester, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

# === Inicializa SPI y configuración de pines ===
BOARD.setup()
lora = LoraTester(verbose=False)

print("\U0001F50C Leyendo registro de versión del SX127x...")
time.sleep(0.1)

try:
    version = lora.get_register(REG_VERSION)
    print(f"\U0001F4E1 Valor RegVersion leído: 0x{version:02X}")

    if version == 0x12:
        print("\u2705 SX1276/SX1278 detectado correctamente.")
    elif version == 0x22:
        print("\u2705 SX1272 detectado correctamente.")
    else:
        print("\u274C Valor inesperado. Puede haber un error de conexión SPI o alimentación.")

except Exception as e:
    print(f"\u26A0\uFE0F Error accediendo al módulo LoRa: {e}")

finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()