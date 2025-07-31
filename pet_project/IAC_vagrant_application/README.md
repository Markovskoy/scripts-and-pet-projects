# Проект: IAC\_VAGRANT\_APPLICATION

## Описание

Этот проект демонстрирует одну из возможных реализаций **Infrastructure as Code (IaC)** с помощью **Vagrant** и **VirtualBox** для локальной разработки и тестирования. Здесь разворачивается виртуальная машина, на которую автоматически устанавливаются и запускаются frontend и backend части приложения.

* **Frontend** разворачивается через **Nginx** и отображает веб-интерфейс
* **Backend** запускается через **systemd unit** и обрабатывает API

## Стек

* Vagrant
* VirtualBox
* Ubuntu 20.04
* OpenJDK 17
* Nginx
* systemd

## Структура проекта

```
IAC_VAGRANT_APPLICATION/
├── Vagrantfile
├── bootstrap.sh
├── setup.sh
├── systemd/
│   └── backend.service     # unit-файл backend
├── backend/                # синхронизируемый артефакт backend
├── frontend/               # синхронизируемый артефакт frontend
└── About.md                # описание проекта
```

## Что делает каждый файл

### `Vagrantfile`

* Создает VM
* Назначает ей:

  * box: Ubuntu 20.04
  * CPU: 2 ядра
  * RAM: 1024 MB
* Пробрасывает порты: 8080 (backend), 80 (frontend)
* Синхронизирует директории backend и frontend
* Вызывает `bootstrap.sh` и `setup.sh`при provision

### `bootstrap.sh`

* Устанавливает зависимости: openjdk-16, nginx
* Создает пользователей, директории и выдает права
* Подготавливает среду

### `setup.sh`

* Копирует jar-файл backend в целевую директорию
* Копирует frontend-файлы в папку nginx
* Копирует unit-файл backend
* Создает nginx-конфиг и активирует
* Запускает systemctl enable + restart
* Настраивает iptables

### `systemd/backend.service`

* Unit-файл для запуска backend как сервиса systemd

## Запуск проекта

1. Скопируйте все артефакты (собранные frontend + backend jar) в соответствующие папки

2. Запуск:

```
vagrant up --provision
```

или:

```
vagrant reload --provision
```

3. Проверка:

```
curl http://localhost:8080
curl http://localhost
```

4. Откройте в браузере:

* [http://localhost:8080](http://localhost:8080)
* [http://localhost](http://localhost)

## Warning

Vagrant используется только для **локальной виртуализации** и тестирования.
