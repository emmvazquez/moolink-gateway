# lora_receiver.py
###
'''
import LoRa  # Usa la librería LoRa compatible que manejes
import config

class LoRaReceiver:
    def __init__(self):
        LoRa.begin(config.RF_FREQUENCY)
        LoRa.setSpreadingFactor(config.LORA_SPREADING_FACTOR)
        LoRa.setSignalBandwidth(config.LORA_BANDWIDTH)
        LoRa.setCodingRate4(config.LORA_CODING_RATE)
        LoRa.setSyncWord(config.LORA_SYNC_WORD)

    def receive_packet(self):
        packet_size = LoRa.parsePacket()
        if packet_size:
            packet = ""
            while LoRa.available():
                packet += chr(LoRa.read())
            return packet
        return None

    def close(self):
        LoRa.end() '''

import time

class LoRaReceiver:
    def __init__(self):
        print("Simulador de recepción LoRa iniciado.")

    def receive_packet(self):
        # Simular un paquete cada 10 segundos
        time.sleep(10)
        simulated_packet = '{"gps_latitude":23.4567,"gps_longitude":-100.1234,"humedad":45.2,"temperatura":39.7,"ritmo_cardiaco":125,"acelerometro_x":0.01,"acelerometro_y":0.02,"acelerometro_z":0.99,"id_bovino":"BOV1234"}'
        return simulated_packet

    def close(self):
        print("Simulador cerrado.")