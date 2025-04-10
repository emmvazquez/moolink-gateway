# 📚 Bitácora de Progreso - MooLink Gateway

Proyecto de monitoreo de ganado usando sensores LoRa y Raspberry Pi.

---

## 📅 Avances por fecha

---

### 2025-04-10

- 🛠️ Se configuró la Raspberry Pi 3:
  - Instalación de Raspberry Pi OS Lite (sin escritorio).
  - Activación de SSH y SPI.
  - Conexión y acceso remoto exitoso vía SSH.

- 📦 Se creó el repositorio en GitHub `moolink-gateway`.
  - Estructura inicial:
    - `main.py`
    - `lora_receiver.py`
    - `data_analyzer.py`
    - `alert_sender.py`
    - `utils.py`
    - `config.py`
    - `requirements.txt`
    - `scripts/update_gateway.sh`
    - `README.md`

- 🧪 Se creó simulador de recepción LoRa:
  - `lora_receiver.py` simula recepción de paquetes JSON cada 10 segundos.

- 🧠 Se implementó análisis de datos:
  - Análisis de:
    - Ritmo cardiaco.
    - Temperatura.
    - Movimiento (acelerómetro).
    - Ubicación GPS (área segura).

- 🚀 Se configuró el arranque automático:
  - Uso de `crontab` para lanzar `main.py` al reiniciar Raspberry.

---

### 2025-04-11

- 📋 Planeación de WebService receptor:
  - Estructura propuesta con Flask.
  - Endpoint `POST /api/eventos`.
  - Guardado de eventos recibidos en archivos JSON.
  - Definición de `moo_webservice/` como nuevo módulo.

- 🔥 Se decidió documentar el avance:
  - Creación del archivo `PROGRESO.md` como bitácora oficial.

---

## 🚀 Siguientes pasos planeados

- [ ] Implementar `moo_webservice/` en Flask.
- [ ] Conexión real de módulo LoRa (SPI) para recepción de paquetes reales.
- [ ] Redireccionar salida de `main.py` a logs controlados.
- [ ] Implementar dashboard web básico para visualización de eventos.
- [ ] Preparar aplicación móvil Android para recepción de alertas.

---

# 📢 Notas importantes

- Se mantiene control de versiones en GitHub.
- El proyecto se ejecuta 100% en modo consola (sin entorno gráfico).
- Se prioriza rendimiento, estabilidad y modularidad.

---

# 🐂 MooLink Gateway en construcción 🛠️
