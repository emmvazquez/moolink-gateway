from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD

BOARD.setup()

lora = LoRa(verbose=False)

# Leer registro versión
version = lora.spi.xfer([0x42 & 0x7F, 0x00])  # 0x42 es RegVersion
print(f"Versión del chip SX127x: {version}")

BOARD.teardown()
