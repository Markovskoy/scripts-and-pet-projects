# Monitoring Infrastructure for Any Application

**Полноценный стек мониторинга и логирования**, готовый для продакшен и pet-проектов.

Проект позволяет:

* Отслеживать состояние любых Linux-серверов
* Собирать логи из Docker-контейнеров
* Собирать системные метрики и кастомные данные
* Визуализировать всё это в Grafana

> Весь стек разворачивается автоматически через Ansible или вручную.

---

## Стек технологий

| Компонент      | Назначение                                        |
| -------------- | ------------------------------------------------- |
| **Prometheus** | Сбор системных метрик с app и monitoring-серверов |
| **Loki**       | Сбор логов контейнеров через Promtail             |
| **Promtail**   | Агент логов, собирает docker-логи                 |
| **Grafana**    | Дашборды и визуализация                           |
| **Ansible**    | Автоматическое развёртывание всей инфраструктуры  |

---

## Требования

* Два Linux-сервера (или виртуалки)
* SSH-доступ к ним
* Ansible (если используешь автоматизацию)

---

## Скриншоты

### 🔹 Grafana: дашборд логов

<img width="1595" height="754" alt="image" src="https://github.com/user-attachments/assets/875cd137-831d-4ff5-99a1-0b77f1fd0759" />

### 🔹 Grafana: состояние серверов
<img width="1626" height="742" alt="image" src="https://github.com/user-attachments/assets/37d473a1-7fb6-4ddf-991d-8ccbfca8bdb8" />


### 🔹 Grafana: мониторинг Java приложения
 <img width="1618" height="804" alt="image" src="https://github.com/user-attachments/assets/467a75b3-47a1-49f0-9605-d56cf87b6fed" />

---

## Структура проекта

```bash
monitoring-project/
├── README.md                       # ← Вы здесь
├── app_server/                     # Реальная структура APP-сервера (ручная настройка)
├── monitoring_server/             # Как настроен monitoring-сервер вручную
├── automatization_by_ansible/     # Полная автоматизация через Ansible
│   └── ansible.md                 # ← Отдельная инструкция по Ansible
```

---

## Варианты использования

### Ручной режим (обучение, портфолио, тест)

В папках `app_server/` и `monitoring_server/` — показываются, как устроены файлы на реальных серверах:

* где лежат конфиги (`/etc/promtail`, `/opt/monitoring`)
* какие systemd-сервисы настроены
* как всё запускается и организовано

---

### Автоматический режим (боевой запуск)

Для автоматического разворачивание на севрераз — используется [`automatization_by_ansible/`](https://github.com/Markovskoy/scripts-and-pet-projects/tree/main/pet_project/monitoring-project/03_automatization_by_ansible).

Там можно найти следующее:

* Ansible playbook
* Роли для app и monitoring серверов
* Дашборды Grafana
* Инструкцию по запуску: [`ansible.md`](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/pet_project/monitoring-project/03_automatization_by_ansible/README.md)

---


