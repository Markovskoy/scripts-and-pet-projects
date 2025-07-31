#!/bin/bash
set -e

# Обновление пакетов и установка зависимостей
apt update && apt install -y openjdk-16-jdk nginx

# Создание пользователя backend (без пароля, с шеллом bash)
useradd -m -s /bin/bash backend || true

# Создание директорий для логов и отчётов + назначение прав
mkdir -p /var/sausage-store/{logs,reports}
chown -R backend:backend /var/sausage-store

# Директории под бинарники и фронтенд
mkdir -p /opt/sausage-store/bin
mkdir -p /opt/frontend

echo " Bootstrap Done."
