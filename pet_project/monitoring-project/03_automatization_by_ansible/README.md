# Ansible: Автоматизация мониторинга

Этот раздел проекта позволяет полностью автоматизировать развёртывание мониторинга на двух серверах (APP и Monitoring) через **одну команду Ansible**.

---

## Что входит в автоматизацию

* Установка Promtail на APP-сервере (через Docker Compose)
* Настройка сбора логов контейнеров
* Установка `node_exporter.service` на оба сервера
* Разворачивание **Grafana + Loki + Prometheus** на Monitoring-сервере
* Загрузка собственных дашбордов в Grafana через API

---

## Структура папки `automatization_by_ansible/`

```
automatization_by_ansible/
├── ansible.md               # ← Эта инструкция
├── site.yml                 # Главный Ansible-плейбук
├── inventory/hosts.yml      # Инвентарь (группы: apps, monitoring)
├── group_vars/              # Переменные по группам
├── roles/                   # Роли для серверов
│   ├── app/                 # Promtail + Node Exporter на APP-сервер
│   ├── monitoring/          # Prometheus, Grafana, Loki
│   └── grafana_dashboards/ # Импорт JSON-дэшбордов в Grafana
```

---

## Быстрый старт

1. Убедитесь, что у вас есть **Ansible** на локальной машине:

```bash
ansible --version
```

2. Перейдите в папку:

```bash
cd automatization_by_ansible
```

3. Запустите playbook:

```bash
ansible-playbook -i inventory/hosts.yml site.yml
```

4. Ansible спросит вас:

```
Введите IP APP-сервера (в формате x.x.x.x):
Введите IP Monitoring-сервера (в формате x.x.x.x):
```

После чего развернёт весь стек по шагам.

---

## Как это работает

* Ansible **копирует все нужные файлы** на сервера (конфиги, docker-compose, systemd)
* Запускает `setup.sh` на каждом сервере
* Monitoring-сервер разворачивает Grafana, Loki, Prometheus в `/opt/monitoring`
* APP-сервер запускает Promtail в контейнере из `/etc/promtail`
* Все логи и метрики поступают в Grafana автоматически

---

## Возможности

* Разворачивание на любые сервера с Linux (Ubuntu, Debian, CentOS)
* Поддержка Docker Compose V2
* Весь стек собирается без ручных шагов
* Легко масштабируется под продакшен

---

## Рекомендации

* Лучше запускать playbook **с локального ansible-сервера** или своей машины
* Убедитесь, что у всех серверов открыт порт `22` (SSH) и `3000/3100/9090` (Grafana, Loki, Prometheus)
* После развёртывания зайдите в Grafana: `http://<monitoring_ip>:3000`

  * Логин: `admin`
  * Пароль: `admin`

---

## Основной проект

Это автоматизация для основного проекта:
  [`../README.md`](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/pet_project/README.md)

---

## Готово!

🔧 Настраивай. Мониторь. Автоматизируй.

— Проект `monitoring-project`
