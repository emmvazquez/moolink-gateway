import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import REG

# === Inicializar board ===
BOARD.setup()

class LoraTester(LoRa):
    def __init__(self, verbose=False):
        super(LoraTester, self).__init__(verbose)
        self.set_mode(LoRa.MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

# Instanciar objeto
lora = LoraTester(verbose=False)

print("\U0001F50C Leyendo registro de versi\u00f3n del SX1278...")

# Leer el registro RegVersion
version = lora.get_reg(REG.VERSION)
print(f"\U0001F4BB Valor RegVersion: {hex(version)}")

# Diagnosticar resultado
if version == 0x12:
    print("\u2705 SX1278 detectado correctamente. SPI funcionando.")
elif version in (0x22, 0x42):
    print("\u26a0\ufe0f SX127x detectado, pero no exactamente SX1278. Puede ser un clone.")
else:
    print("\u274C Error: No se detect\u00f3 el SX1278. Revisa conexiones SPI o alimentaci\u00f3n.")

# Finalizar
BOARD.teardown()
