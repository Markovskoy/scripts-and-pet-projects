# GitLab CI/CD Pipeline: Static Analysis + Telegram Notifications

> Автоматизация сборки и анализа frontend/backend с уведомлениями

## Описание 

CI/CD пайплайны в GitLab для типового fullstack-приложения (Java + TypeScript). 
Пайплайн включает:

- сборку кода;
- статический анализ безопасности и качества кода;
- публикацию артефактов;
- уведомления о сборке в Telegram.

###  Основные возможности

-  **Сборка backend (Java + Maven)** и **frontend (TypeScript + npm)**
-  **SAST-проверки**: `semgrep`, `nodejs-scan`, `SonarQube` (отдельно для фронта и бэка)
-  **Уведомления в Telegram** по ключевым коммитам
-  **Отчёты SonarQube**: качество, баги, покрытия, дубликаты

---

## ⚙️ Технологии и инструменты

| Категория     | Инструменты                                             |
|---------------|----------------------------------------------------------|
| CI/CD         | GitLab CI/CD                                             |
| Backend       | Java 16, Maven                                           |
| Frontend      | TypeScript, Node.js, npm                                 |
| Статический анализ | Semgrep, Nodejs-scan, SonarQube                     |
| Отчёты        | SonarScanner CLI, Maven Sonar Plugin                     |
| Уведомления   | Telegram Bot API                                         |

---

## Архитектура пайплайна

<img width="759" height="303" alt="image" src="https://github.com/user-attachments/assets/0b6b3f38-2a40-4f7e-b699-648e6a8498cc" />

## SonarQube отчёты

<img width="986" height="324" alt="image" src="https://github.com/user-attachments/assets/6e968ed9-c5ac-4c67-aa2f-caafde996556" />


