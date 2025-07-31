#!/bin/bash
set -e

echo "[1/4] Проверяем docker и docker-compose..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установи его вручную."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose V2 не найден. Установи или настрой alias."
    exit 1
fi

echo "[2/4] Создаём директорию /etc/promtail..."
mkdir -p /etc/promtail

echo "[3/4] Копируем конфиги promtail и docker-compose..."
cp ./promtail-config.yaml /etc/promtail/config.yaml
cp ./docker-compose.promtail.yml /etc/promtail/docker-compose.yml
touch /etc/promtail/positions.yaml

echo "[4/4] Запускаем Promtail через docker-compose..."
cd /etc/promtail
docker compose up -d

echo "✅ Promtail успешно установлен и запущен в контейнере"
