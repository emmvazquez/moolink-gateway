"""
Test: Diagnóstico básico de módulo SX1278 en Raspberry Pi
Fecha: 12 de mayo de 2025
Propósito: Verificar conexión SPI, pines y respuesta del LoRa SX1278
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE
import time

# Desactivar configuración automática de eventos
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaCheck(LoRa):
    def __init__(self):
        super().__init__(verbose=True)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

# Iniciar prueba
print("🔧 Iniciando prueba del módulo SX1278...")

try:
    lora = LoRaCheck()
    print("✅ SX1278 detectado por SPI")

    lora.set_freq(915.0)
    lora.set_spreading_factor(7)
    lora.set_bw(7)
    lora.set_coding_rate(1)
    lora.set_preamble(8)
    lora.set_sync_word(0x12)
    lora.set_rx_crc(True)

    lora.set_mode(MODE.STDBY)
    print("✅ Configuración básica aplicada")
    
    lora.set_mode(MODE.RXCONT)
    print("📡 Listo para recibir (modo continuo)")
    
    for i in range(5):
        flags = lora.get_irq_flags()
        print(f"⏳ Flags ciclo {i+1}: {flags}")
        time.sleep(1)

    print("✅ Prueba terminada correctamente")

except Exception as e:
    print("❌ ERROR:", e)
