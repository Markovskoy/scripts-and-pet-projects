[![View Repo](https://img.shields.io/badge/GitHub-Посмотреть_репозиторий-181717?logo=github)](https://github.com/Markovskoy/scripts-and-pet-projects)


![Purpose](https://img.shields.io/badge/type-Portfolio-important)
![Status](https://img.shields.io/badge/status-Demo-lightgrey)  

![Bash](https://img.shields.io/badge/Bash-4EAA25?logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-000000?logo=ansible&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab_CI-FC6D26?logo=gitlab&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)

  Я начинающий DevOps-инженер,  владею инструментами автоматизации, мониторинга и CI/CD.  
  Активно развиваюсь в сфере DevOps, внедряю автоматизация на работе и создаю pet-проекты, приближённые к боевым условиям.

  В этом портфолио собраны:
- практические решения на Ansible, Docker, GitLab CI/CD, Prometheus, Grafana и др.
- демонстрации настройки инфраструктуры, мониторинга и автоматизации
- скрипты и проекты, использовавшиеся в реальной практике

## Контакты

[![Email](https://img.shields.io/badge/email-v__markovskoy%40mail.ru-blue?logo=gmail&logoColor=white)](mailto:v_markovskoy@mail.ru)
[![Telegram](https://img.shields.io/badge/Telegram-@Markovskoy-blue?logo=telegram)](https://t.me/Vixxt0r)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Victor%20Markovskoy-blue?logo=linkedin)](https://www.linkedin.com/in/viktor-markovskoy-9b2b522b9)

---
###  Примеры проектов

| 📊 Monitoring Stack | 🛠️ GitLab CI/CD | ⚙️ Python-скрипты |
|---------------------|------------------|---------------------|
| Prometheus, Grafana, Loki | Полный пайплайн: frontend + backend + deploy | Отправка файлов по SSH на кластеры |

Подробнее ниже ⬇

---

##  Содержание репозитория
```bash
Repo/
├── work_scripts/               # Автоматизация и полезные скрипты
│   ├── ansible_project/        # Ansible скрипты дла автоматизации задач на нескольких серверах
│   ├── bash_scripts/           # CLI-утилиты, работа с Zabbix
│   ├── powershell_scripts/     # Windows-инструменты и диагностика
│   ├── python_scripts/         # Автоматизация
│   ├── sql_scripts/            # Аналитика и мониторинг БД
│   └── ci_cd/                  # CI/CD пайплайны и конфигурации
│       ├── gitlab/             # GitLab CI: .gitlab-ci.yml, шаблоны и скрипты
│       └── jenkins/            # Jenkins: pipeline'ы, конфиги, groovy-скрипты
│          
└── pet_project/                # Учебные и демонстрационные мини-проекты
    ├── monitoring-project      # Полноценный стек мониторинга и логирования
    ├── сomand_to_server        # Python-инструмент для отправки файлов и выполнения команд на множестве серверов
    └── IAC_vagrant_application # Реализаций IaC с помощью Vagrant и VirtualBox
```

##  Демонстрационные кейсы

| Тип           | Пример                                                                                      | Назначение                                                                 |
|----------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
|  Bash         | [khd.sh](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/work_scripts/bash_scripts/khd.sh)  | Мониторинг ETL, интеграция с Zabbix                                       |
|  Python       | [command_to_server](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/pet_project/command_to_server/) | Инструмент отправки команд/файлов на множественные серверы через SSH |
|  IaC / Vagrant | [IAC_vagrant_application](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/pet_project/IAC_vagrant_application/) | Развёртывание среды через Vagrant + systemd + nginx                      |

###  Monitoring Stack (Prometheus + Grafana + Promtail + Loki)

 [Исходники и конфиги](https://github.com/Markovskoy/scripts-and-pet-projects/blob/main/pet_project/monitoring-project/)

Используемые технологии: Docker, Prometheus, Grafana, Loki, Promtail  
 
Цель: мониторинг backend/frontend + логирование контейнеров

####  Скриншот дашбордов Grafana

<div style="display: flex; gap: 10px; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/875cd137-831d-4ff5-99a1-0b77f1fd0759" width="49%" />
  <img src="https://github.com/user-attachments/assets/37d473a1-7fb6-4ddf-991d-8ccbfca8bdb8" width="49%" />
</div>



### CI/CD Fullstack Pipeline (GitLab)

 [Исходники и конфиги](https://github.com/Markovskoy/scripts-and-pet-projects/tree/main/work_scripts/ci_cd/gitlab/fullstack_ci)
 
Используемые технологии: GitLab CI/CD, Maven, npm, , Semgrep, Nodejs-scan, SonarQube
 
Цель: автоматическая сборка frontend и backend, статический анализ безопасности и качества кода, генерация артефактов и уведомление в телеграмме

####  Пример пайплайна в GitLab
<img width="801" height="267" alt="image" src="https://github.com/user-attachments/assets/d7aa67d3-4cfe-40da-95b2-9b5f9bf7f171" />

#### SonarQube отчёты

<img width="986" height="324" alt="image" src="https://github.com/user-attachments/assets/6e968ed9-c5ac-4c67-aa2f-caafde996556" />

---

##  Ключевые навыки и инструменты

- **Языки и технологии:**  
  Bash, Python, PowerShell, SQL (Oracle, MSSQL)

- **Контейнеризация и оркестрация:**  
  Docker, Docker Compose

- **Инфраструктура как код (IaC):**  
  Ansible, Vagrant

- **CI/CD и управление сборкой:**  
  GitLab CI/CD, Jenkins, Git

- **Мониторинг и логирование:**  
  Zabbix, Zabbix Agent, Prometheus, Grafana, Loki, Promtail

- **DevOps-инженерия:**  
  Написание CLI-утилит, автоматизация задач, работа с логами, cron, systemd
---

##  Примечание

Все проекты и скрипты в этом портфолио:
- либо применялись в реальных задачах на работе,
- либо разработаны как pet-проекты для  демонстрации и изучения DevOps-инструментов.

Каждый пример максимально приближен к боевым условиям — с рабочими пайплайнами, конфигурацией, логированием и мониторингом.
