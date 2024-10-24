# Text Analyzer Project

## Описание проекта
Это веб-приложение для анализа текста, которое выполняет автоматическую суммаризацию текста и выделение ключевых слов с использованием моделей искусственного интеллекта (ИИ). Приложение поддерживает загрузку файлов в формате PDF, DOCX и TXT и предоставляет результаты анализа в виде аннотации текста и списка ключевых понятий.

---

## Установка и запуск проекта

Следуйте этим шагам для установки и запуска проекта на вашем локальном компьютере.

## 1. Клонирование проекта
Склонируйте репозиторий с GitHub на ваш компьютер. Откройте терминал или командную строку и выполните следующую команду:

```bash
git clone https://github.com/your-username/text-analyzer-project.git
```

## 2. Перейдите в директорию проекта
```bash 
cd text-analyzer-project/src
```

## 3. Создание виртуального окружения
Для предотвращения конфликтов с другими проектами создайте виртуальное окружение Python:

- **Windows**:
    ```bash
    python -m venv venv
    ```

- **macOS/Linux**:
    ```bash
    python3 -m venv venv
    ```

Активируйте виртуальное окружение:

- **Windows**:
    ```bash
    venv\Scripts\activate
    ```

- **macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

## 4. Установка зависимостей

После активации виртуального окружения установите все зависимости, указанные в файле `requirements.txt`:

```bash
pip install fastapi uvicorn jinja2 transformers torch keybert langdetect python-docx PyPDF2
 ```


## 5. Запуск приложения
Для запуска приложения используйте следующую команду:

```bash
uvicorn app:app --reload
 ```

## 6. Открытие приложения
После запуска сервера откройте браузер и перейдите по адресу:

```bash
http://127.0.0.1:8000
```

## 7. Остановка сервера
Чтобы остановить сервер, нажмите CTRL + C в терминале.

## 8. Деактивация виртуального окружения
Чтобы выйти из виртуального окружения, выполните команду:
```bash
deactivate
```
