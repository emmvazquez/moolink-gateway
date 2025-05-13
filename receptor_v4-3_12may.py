"""
Proyecto: MooLink - Receptor LoRa + Envío API
Fecha: 12 mayo 2025
Versión: 4.3
Descripción:
Recibe datos desde ESP32-S3 por LoRa y los envía a la API como JSON.
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time
import requests

# === Configuración API ===
API_URL = "https://moolink.e-icus.net/api/localizacion"

# Desactivar conflictos en setup
BOARD.setup = lambda: None
BOARD.add_events = lambda *args, **kwargs: None
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self):
        super().__init__(verbose=False)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

def enviar_a_api(datos):
    try:
        response = requests.post(API_URL, json=datos, timeout=5)
        if response.status_code == 201:
            print("✅ Datos enviados a la API")
        else:
            print("⚠️ Error al enviar a API:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error de conexión API:", e)

def convertir_a_json(payload_str):
    try:
        campos = payload_str.split(',')
        if len(campos) != 13:
            print("⚠️ Formato inesperado, campos:", len(campos))
            return None

        return {
            "idBovino": int(campos[0]),
            "temperatura": float(campos[1]),
            "humedad": float(campos[2]),
            "latitud": float(campos[3]),
            "longitud": float(campos[4]),
            "ritmo_cardiaco": float(campos[5]),
            "ax": float(campos[6]),
            "ay": float(campos[7]),
            "az": float(campos[8]),
            "gx": float(campos[9]),
            "gy": float(campos[10]),
            "gz": float(campos[11])
        }
    except Exception as e:
        print("❌ Error al convertir mensaje:", e)
        return None

# === Inicializar LoRa ===
lora = LoRaReceiver()
lora.set_freq(915.0)
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor LoRa + Envío API listo...\n")

try:
    while True:
        flags = lora.get_irq_flags()
        if flags.get('rx_done'):
            lora.clear_irq_flags(RxDone=1)
            raw = bytes(lora.read_payload(nocheck=True))
            print("📦 Recibido:", raw)

            if raw.startswith(b'@') and raw.endswith(b'#'):
                payload_str = raw[1:-1].decode('utf-8', errors='ignore')
                print("✅ Mensaje válido:", payload_str)

                datos = convertir_a_json(payload_str)
                if datos:
                    enviar_a_api(datos)
            else:
                print("⚠️ Delimitadores no válidos")

        time.sleep(0.1)

except KeyboardInterrupt:
    lora.set_mode(MODE.SLEEP)
    print("\n⛔ Programa interrumpido")
