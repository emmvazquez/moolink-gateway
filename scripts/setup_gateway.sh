#!/bin/bash

echo "====================================="
echo " Instalador automático MooLink Gateway"
echo " Raspberry Pi 3 - Sistema Lite"
echo "====================================="

# Variables
MOO_REPO="https://github.com/emmvazquez/moolink-gateway.git"
MOO_DIR="$HOME/moo_receptor"

# 1. Actualizar sistema
echo "[1/5] Actualizando sistema operativo..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar git, python3 y pip3
echo "[2/5] Instalando Git, Python3 y Pip3..."
sudo apt install -y git python3 python3-pip

# 3. Instalar librerías necesarias
echo "[3/5] Instalando dependencias de Python..."
pip3 install spidev RPi.GPIO requests scikit-learn joblib

# 4. Clonar o actualizar repositorio
if [ ! -d "$MOO_DIR" ]; then
    echo "[4/5] Clonando repositorio MooLink Gateway..."
    git clone "$MOO_REPO" "$MOO_DIR"
else
    echo "[4/5] Repositorio ya existe, actualizando..."
    cd "$MOO_DIR"
    git pull
fi

# 5. Configurar ejecución automática al encender (crontab)
echo "[5/5] Configurando ejecución automática..."

CRON_CMD="@reboot cd $MOO_DIR && git pull && python3 main.py"
(crontab -l 2>/dev/null; echo "$CRON_CMD") | grep -v "no crontab" | sort -u | crontab -

echo "====================================="
echo " MooLink Gateway instalado correctamente!"
echo " Por favor, reinicia la Raspberry Pi. 🚀"
echo "====================================="
