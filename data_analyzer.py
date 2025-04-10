# data_analyzer.py

import config
import utils

class DataAnalyzer:
    def __init__(self):
        pass

    def check_anomaly(self, data):
        alerta = False
        tipo_alerta = "normal"
        mensaje_alerta = "Todo en parámetros normales."

        bpm = data.get('ritmo_cardiaco')
        temperatura = data.get('temperatura')
        acc_x = data.get('acelerometro_x', 0)
        acc_y = data.get('acelerometro_y', 0)
        acc_z = data.get('acelerometro_z', 0)
        gps_lat = data.get('gps_latitude')
        gps_lon = data.get('gps_longitude')

        aceleracion_total = (acc_x**2 + acc_y**2 + acc_z**2)**0.5

        if bpm and (bpm < 40 or bpm > 120):
            alerta = True
            tipo_alerta = "ritmo_cardiaco_anormal"
            mensaje_alerta = f"Ritmo cardiaco anormal: {bpm} bpm."

        if temperatura and (temperatura < 37.5 or temperatura > 39.5):
            alerta = True
            tipo_alerta = "temperatura_anormal"
            mensaje_alerta = f"Temperatura anormal: {temperatura} °C."

        if aceleracion_total > 2.0:
            alerta = True
            tipo_alerta = "actividad_intensa"
            mensaje_alerta = f"Movimiento intenso detectado ({aceleracion_total:.2f} G)."

        if gps_lat and gps_lon:
            distancia = utils.distancia_metros(
                gps_lat, gps_lon, config.AREA_CENTRO_LAT, config.AREA_CENTRO_LON
            )
            if distancia > config.AREA_RADIO_METROS:
                alerta = True
                tipo_alerta = "fuera_area_segura"
                mensaje_alerta = f"Bovino fuera del área segura ({distancia:.2f} metros)."

        return alerta, tipo_alerta, mensaje_alerta
