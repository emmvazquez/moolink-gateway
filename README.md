# MooLink Gateway (Raspberry Pi 3)

Sistema de recepción de datos LoRa y envío de alertas desde bovinos equipados.

## Funcionalidades
- Recepción de datos LoRa (ESP32-S3 -> SX1262).
- Análisis de anomalías (temperatura, ritmo cardiaco, ubicación GPS).
- Envío de eventos a un WebService.
- Registro local de eventos en logs rotativos.

## Requisitos
- Raspberry Pi 3 o superior.
- Módulo LoRa conectado por SPI.
- Python 3 instalado.

## Instalación
```bash
pip3 install -r requirements.txt
