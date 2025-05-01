from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time
import RPi.GPIO as GPIO

# Definir manualmente los factores de propagación (Spreading Factors)
class SF:
    SF7 = 7
    SF8 = 8
    SF9 = 9
    SF10 = 10
    SF11 = 11
    SF12 = 12

# Anular eventos automáticos antes de iniciar
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

    def set_bandwidth(self, bw):
        self.set_bw(bw)

BOARD.setup()

lora = LoRaReceiver(verbose=False)

# Configuración LoRa compatible con emisor MooLink
lora.set_freq(915.0)
lora.set_spreading_factor(SF.SF12)
lora.set_bandwidth(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_preamble(8)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

lora.set_mode(MODE.RXCONT)
print("📡 Receptor SX1276 en modo RXCONT sin interrupciones...")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            payload = lora.read_payload(nocheck=True)
            print("📦 Bytes crudos:", payload)

            try:
                mensaje = bytes(payload).decode('utf-8').strip()
                print("📨 Texto recibido:", mensaje)

                # Si se detecta que el mensaje es tipo JSON
                if mensaje.startswith("{") and mensaje.endswith("}"):
                    import json
                    try:
                        data = json.loads(mensaje)
                        print("✅ JSON válido:", data)
                    except json.JSONDecodeError:
                        print("⚠️ JSON inválido, pero UTF-8 válido")
                # Si se detecta CSV
                elif "," in mensaje:
                    partes = mensaje.split(",")
                    print("📊 CSV recibido:", partes)
                else:
                    print("📃 Texto plano recibido:", mensaje)

            except UnicodeDecodeError:
                print("❌ No se pudo decodificar como UTF-8")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n⛔ Interrumpido por el usuario.")
finally:
    lora.set_mode(MODE.SLEEP)
    GPIO.cleanup()
