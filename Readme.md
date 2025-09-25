
---

# 🎓 Alumni API (Django + DRF + PostgreSQL + Docker)

Бэкенд для Alumni-платформы: новости, отзывы, регистрация и авторизация пользователей (JWT, Djoser).
API полностью готово к локальной разработке и продакшн через Docker.

---

## 📌 Стек

* Python 3.12
* Django 5 + DRF
* PostgreSQL
* JWT (SimpleJWT)
* Djoser — готовые эндпоинты для регистрации/логина
* Swagger — документация API
* Docker / Docker Compose

---

## ⚡️ 1. Установка зависимостей

Убедись, что установлены:

* [Python 3.12+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/) и Docker Compose (если планируется запуск в контейнере)
* (опционально) PostgreSQL — если работаешь без Docker

---

## ⚡️ 2. Клонирование репозитория

```bash
git clone https://github.com/yourusername/alumni.git
cd alumni
```

---

## ⚡️ 3. Настройка окружения

Создай файл **.env** в корне проекта (рядом с `docker-compose.yml`):

```env
DEBUG=True
SECRET_KEY=super_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=alumni_db
POSTGRES_USER=alumni_user
POSTGRES_PASSWORD=alumni_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

> ⚠️ Для продакшена: выстави `DEBUG=False`, придумай уникальный `SECRET_KEY` и используй реальные хосты в `ALLOWED_HOSTS`.

---

## 🖥 4. Локальный запуск (без Docker)

### 4.1 Создание виртуального окружения и установка зависимостей

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4.2 Настройка базы данных

Создай базу PostgreSQL и пользователя:

```sql
CREATE DATABASE alumni_db;
CREATE USER alumni_user WITH PASSWORD 'alumni_pass';
GRANT ALL PRIVILEGES ON DATABASE alumni_db TO alumni_user;
```

> Не забудь в `.env` поменять `POSTGRES_HOST` на `localhost`, если работаешь локально.

---

### 4.3 Миграции и статика

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

### 4.4 Создание суперпользователя

```bash
python manage.py createsuperuser
```

---

### 4.5 Запуск сервера

```bash
python manage.py runserver
```

API будет доступно на:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐳 5. Запуск через Docker

### 5.1 Сборка контейнеров

```bash
docker compose build
```

### 5.2 Запуск контейнеров

```bash
docker compose up -d
```

### 5.3 Создание суперпользователя (первый раз)

```bash
docker compose exec web python manage.py createsuperuser
```

После запуска:

* API → [http://localhost:8000/api/](http://localhost:8000/api/)
* Swagger → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* Админка → [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔑 6. Авторизация

Используется JWT:

* Получить токен: `POST /auth/login/`
* Обновить токен: `POST /auth/token/refresh/`

> В заголовках запроса указывать:

```
Authorization: Bearer <access_token>
```

---

## 📂 7. Основные эндпоинты

| Метод | URL                    | Описание                        |
| ----- | ---------------------- | ------------------------------- |
| POST  | `/auth/register/`      | Регистрация с автологином       |
| POST  | `/auth/login/`         | Получение JWT токена (логин)    |
| POST  | `/auth/token/refresh/` | Обновление access токена        |
| GET   | `/news/`               | Список новостей (доступно всем) |
| POST  | `/feedback/`           | Отправка отзыва (доступно всем) |
| GET   | `/feedback/`           | Список отзывов (только админ)   |
| GET   | `/auth/me/`            | Просмотр своего профиля         |
| GET   | `/graduates/`          | Список выпускников              |

---

## ⚙️ 8. Полезные команды Docker

| Команда                        | Действие                               |
| ------------------------------ | -------------------------------------- |
| `docker compose logs -f`       | Логи всех контейнеров                  |
| `docker compose exec web bash` | Зайти внутрь контейнера Django         |
| `docker compose down`          | Остановить контейнеры                  |
| `docker compose down -v`       | Остановить контейнеры и удалить volume |

---

## 📝 Примечания

* Для продакшена **обязательно** поменяй `SECRET_KEY` и `POSTGRES_PASSWORD` в `.env`.
* Если нужен автологин после регистрации — фронтенд хранит JWT (HttpOnly cookie или localStorage).
* Документация Swagger доступна по `/swagger/`.

---


