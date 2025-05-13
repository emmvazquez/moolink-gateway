"""
Proyecto: MooLink - Receptor LoRa con Diagnóstico
Fecha: 12 mayo 2025
Versión: 4.1
Descripción:
1. Diagnostica el módulo SX1278 conectado por SPI.
2. Configura parámetros LoRa punto a punto.
3. Recibe mensajes delimitados tipo @...#.
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time

# Desactivar configuración conflictiva
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self):
        super().__init__(verbose=True)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

# === Diagnóstico del módulo ===
def diagnosticar_lora():
    print("🔧 Iniciando diagnóstico del SX1278...")
    try:
        lora = LoRaReceiver()
        lora.set_mode(MODE.STDBY)
        print("✅ SX1278 detectado por SPI")
        lora.set_mode(MODE.SLEEP)
        return True
    except Exception as e:
        print("❌ Error al detectar módulo SX1278:", e)
        return False

# === Receptor final ===
def receptor_lora():
    print("\n📡 Iniciando receptor LoRa...")
    lora = LoRaReceiver()

    lora.set_freq(915.0)
    lora.set_spreading_factor(7)
    lora.set_bw(BW.BW125)
    lora.set_coding_rate(CODING_RATE.CR4_5)
    lora.set_preamble(8)
    lora.set_sync_word(0x12)
    lora.set_rx_crc(True)

    lora.set_mode(MODE.RXCONT)
    print("✅ Configuración aplicada. Esperando mensajes...\n")

    try:
        while True:
            flags = lora.get_irq_flags()
            if flags.get('rx_done'):
                lora.clear_irq_flags(RxDone=1)
                payload = bytes(lora.read_payload(nocheck=True))

                print("📦 Paquete recibido:", payload)

                if payload.startswith(b'@') and payload.endswith(b'#'):
                    contenido = payload[1:-1].decode('utf-8', errors='ignore')
                    print("✅ Mensaje válido:", contenido)
                else:
                    print("⚠️ Mensaje sin delimitadores válidos")

            time.sleep(0.1)

    except KeyboardInterrupt:
        lora.set_mode(MODE.SLEEP)
        print("\n⛔ Finalizado manualmente")

# === Ejecutar todo ===
if __name__ == "__main__":
    if diagnosticar_lora():
        receptor_lora()
    else:
        print("🛑 Abortando. Verifica el módulo LoRa y reinicia.")
