#!/bin/bash

echo "====================================="
echo " Actualizador de MooLink Gateway"
echo " Raspberry Pi 3 - Sistema Lite"
echo "====================================="

# Variables
MOO_DIR="$HOME/moo_receptor"

# 1. Actualizar sistema operativo (opcional)
echo "[1/4] Actualizando paquetes del sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Actualizar repositorio MooLink
if [ -d "$MOO_DIR" ]; then
    echo "[2/4] Actualizando repositorio MooLink Gateway..."
    cd "$MOO_DIR"
    git pull
else
    echo "Error: No se encontró el directorio $MOO_DIR"
    exit 1
fi

# 3. Actualizar dependencias Python
echo "[3/4] Actualizando dependencias de Python..."
pip3 install --upgrade -r requirements.txt

# 4. Reiniciar servicio MooLink Gateway
echo "[4/4] Reiniciando MooLink Gateway..."

# Matar procesos anteriores de main.py
pkill -f "python3 main.py"

# Volver a lanzar main.py
cd "$MOO_DIR"
nohup python3 main.py > /dev/null 2>&1 &

echo "====================================="
echo " MooLink Gateway actualizado y en ejecución! 🚀"
echo "====================================="
