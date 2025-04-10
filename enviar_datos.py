import time
import requests
import random
from datetime import datetime

# URL de tu servicio web
url = "https://moolink.e-icus.net/api/localizacion/recibir"

# Datos fijos de tu dispositivo / bovino
idBovino = 1
idDispositivo = 1

while True:
    # Generar datos aleatorios simulados
    latitud = round(19.4326 + random.uniform(-0.001, 0.001), 6)
    longitud = round(-99.1332 + random.uniform(-0.001, 0.001), 6)
    humedad = round(random.uniform(50, 70), 2)
    temperatura = round(random.uniform(20, 35), 2)
    ritmo_cardiaco = random.randint(60, 100)
    acel_x = round(random.uniform(-1, 1), 2)
    acel_y = round(random.uniform(-1, 1), 2)
    acel_z = round(random.uniform(9, 10), 2)

    # Construir el paquete de datos
    data = {
        "idBovino": idBovino,
        "idDispositivo": idDispositivo,
        "datos": {
            "gps": {
                "latitud": latitud,
                "longitud": longitud
            },
            "humedad": humedad,
            "temperatura": temperatura,
            "ritmo_cardiaco": ritmo_cardiaco,
            "acelerometro": {
                "x": acel_x,
                "y": acel_y,
                "z": acel_z
            }
        }
    }

    # Enviar los datos
    try:
        response = requests.post(url, json=data)
        print(f"[{datetime.now()}] Enviado: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] Error al enviar datos: {e}")

    # Esperar 60 segundos
    time.sleep(60)
