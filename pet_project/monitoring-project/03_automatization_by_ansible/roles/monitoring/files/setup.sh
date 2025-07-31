#!/bin/bash
set -e

echo "[1/7] Создаём рабочие директории..."

mkdir -p /opt/monitoring/{data/grafana,data/loki,data/prometheus}
mkdir -p /opt/monitoring/configs
mkdir -p /opt/monitoring/dashboards

echo "[2/7] Копируем конфиги Prometheus, Loki и docker-compose..."

cp ./docker-compose.yml /opt/monitoring/docker-compose.yml
cp ./loki-config.yaml /opt/monitoring/configs/loki-config.yaml
cp ./prometheus.yml /opt/monitoring/configs/prometheus.yml

echo "[3/7] Копируем дашборды Grafana..."

cp ./dashboards/*.json /opt/monitoring/dashboards/

echo "[4/7] Выдаём права на каталоги..."

chown -R root:root /opt/monitoring
chmod -R 755 /opt/monitoring

echo "[5/7] Копируем systemd unit node_exporter.service..."

cp ./node_exporter.service /etc/systemd/system/node_exporter.service
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable node_exporter.service
systemctl restart node_exporter.service

echo "[6/7] Переходим в директорию /opt/monitoring и запускаем docker-compose..."

cd /opt/monitoring
docker compose up -d

echo "[7/7] Установка и запуск Monitoring stack завершены!"
