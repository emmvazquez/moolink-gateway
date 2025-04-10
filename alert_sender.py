# alert_sender.py

import requests
import config
import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.expanduser("~/moo_receptor_logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "eventos.log")

logger = logging.getLogger("MooLinkLogger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5*1024*1024,
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AlertSender:
    def __init__(self):
        self.url = config.WEBSERVICE_URL

    def construir_payload(self, data, alerta, tipo_alerta, mensaje_alerta):
        fecha_hora = datetime.datetime.utcnow().isoformat() + "Z"
        id_bovino = data.get("id_bovino", "BOV_DESCONOCIDO")
        evento_id = f"EVT_{fecha_hora.replace(':', '').replace('-', '').replace('T', '_')}_{id_bovino}"

        payload = {
            "evento_id": evento_id,
            "receptor_id": "RPi003",
            "fecha_hora": fecha_hora,
            "bovino": {
                "id": id_bovino
            },
            "alerta": {
                "estado": alerta,
                "nivel": "critico" if alerta else "normal",
                "tipo": tipo_alerta,
                "mensaje": mensaje_alerta
            },
            "datos": {
                "gps": {
                    "latitud": data.get("gps_latitude"),
                    "longitud": data.get("gps_longitude")
                },
                "humedad": data.get("humedad"),
                "temperatura": data.get("temperatura"),
                "ritmo_cardiaco": data.get("ritmo_cardiaco"),
                "acelerometro": {
                    "x": data.get("acelerometro_x"),
                    "y": data.get("acelerometro_y"),
                    "z": data.get("acelerometro_z")
                }
            }
        }

        return payload

    def send_data(self, data, alerta, tipo_alerta, mensaje_alerta):
        payload = self.construir_payload(data, alerta, tipo_alerta, mensaje_alerta)

        if alerta:
            logger.warning(f"ALERTA detectada: {payload['alerta']['tipo']} - {payload['alerta']['mensaje']}")
        else:
            logger.info(f"Evento normal: {payload['alerta']['mensaje']}")

        try:
            response = requests.post(self.url, json=payload, timeout=5)
            if response.status_code != 200:
                logger.error(f"Error enviando datos. Código: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error de conexión: {e}")
