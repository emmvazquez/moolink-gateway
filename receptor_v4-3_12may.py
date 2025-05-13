"""
Proyecto: MooLink - Receptor LoRa + Envío a API REST
Fecha: 12 mayo 2025
Versión: 4.4
Descripción:
Recibe datos desde ESP32-S3 por LoRa en formato @i,temp,hum,lat,lon,bpm,ax,ay,az,gx,gy,gz#
y los envía como JSON a la API REST de MooLink.
"""

from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE, BW, CODING_RATE
import time
import requests
import json

# === Configuración API ===
API_URL = "https://moolink.e-icus.net/api/localizacion"

# === Inicialización segura del board SX1278 ===
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
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(API_URL, json=datos, headers=headers, timeout=5)
        if response.status_code == 201:
            print("✅ Datos enviados a la API")
        else:
            print(f"⚠️ API respondió con error {response.status_code}:\n{response.text}")
    except Exception as e:
        print("❌ Error al conectar con la API:", e)

def convertir_a_json(payload_str):
    try:
        campos = payload_str.split(',')
        if len(campos) != 12:
            print(f"⚠️ Formato inesperado, se esperaban 13 campos, recibidos: {len(campos)}")
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
        print("❌ Error al procesar el mensaje LoRa:", e)
        return None

# === Configuración LoRa SX1278 ===
lora = LoRaReceiver()
lora.set_freq(915.0)
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_mode(MODE.RXCONT)

print("📡 Receptor LoRa + API MooLink iniciado correctamente...\n")

# === Bucle principal ===
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
                    print("📤 Enviando JSON:", json.dumps(datos))
                    enviar_a_api(datos)
            else:
                print("⚠️ Delimitadores ausentes (@...#)")

        time.sleep(0.1)

except KeyboardInterrupt:
    lora.set_mode(MODE.SLEEP)
    print("\n🛑 Recepción detenida manualmente")
