﻿# PlatformEducational
# Django Educational Platform

Добро пожаловать в репозиторий образовательной платформы на Django! Этот проект предназначен для упрощения управления образовательным процессом. Здесь вы найдете инструкции по установке и использованию системы.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Yarik-f/PlatformEducational.git
   cd PlatformEducational
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate # Для Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Выполните миграции базы данных:
   ```bash
   python manage.py migrate
   ```

5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

Теперь приложение доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Основные функции

### 1. Управление пользователями
- При добавлении учителя в админ-панели отправляется письмо на почту с логином и паролем.
- Пользователь автоматически добавляется в группу в зависимости от позиции ("Учитель", "Директор" и т.д.).

### 2. Работа с заявками на поступление
- При подаче заявки пользователь получает письмо с логином и паролем.
- После входа пользователь загружает необходимые документы. Документы автоматически архивируются для просмотра руководством.
- Руководство может:
  - Одобрить заявку: пользователь автоматически добавляется в модель студентов, и создается класс, если он не существует.
  - Отклонить заявку: аккаунт удаляется.

### 3. Личный кабинет
- Студенты могут скачивать доступные документы.
- Все пользователи могут изменить пароль.
- Руководство может:
  - Просматривать списки классов.
  - Назначать классных руководителей.

### 4. Работа с расписанием
- Импорт и экспорт расписания через Excel (используется библиотека OpenPyXL).

### 5. Функции для всех пользователей
- Подать заявку на поступление.
- Задать вопрос через форму.
- Записаться на платные услуги.

### 6. Школьная жизнь
- Раздел "Школьная жизнь" отображает информацию из модели блога, расписания и других форм.

### 7. Основные сведения
- Вкладка содержит общую информацию о школе: контакты, документы, награды, лицензии и т.д.

### 8. API
- Подключение API для сторонних устройств доступно без ключа.

## Используемые технологии
- **Django**: основной фреймворк.
- **OpenPyXL**: работа с Excel-таблицами.

