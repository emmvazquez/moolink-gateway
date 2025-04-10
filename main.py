# main.py

from lora_receiver import LoRaReceiver
from data_analyzer import DataAnalyzer
from alert_sender import AlertSender
import utils
import time

def main():
    try:
        receiver = LoRaReceiver()
        analyzer = DataAnalyzer()
        sender = AlertSender()

        print("Esperando paquetes LoRa...")

        while True:
            packet = receiver.receive_packet()
            if packet:
                data = utils.parse_json(packet)
                if data:
                    alerta, tipo_alerta, mensaje_alerta = analyzer.check_anomaly(data)
                    sender.send_data(data, alerta, tipo_alerta, mensaje_alerta)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nFinalizando programa...")
    finally:
        receiver.close()

if __name__ == "__main__":
    main()
