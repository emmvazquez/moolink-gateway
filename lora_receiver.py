# lora_receiver.py

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
        LoRa.end()
