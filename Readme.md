
---

# 🎓 Alumni API (Django + DRF + PostgreSQL + Docker)

Проект — бэкенд для Alumni-платформы: новости, отзывы, регистрация/авторизация пользователей (JWT, Djoser).

## 📌 Стек

* **Python 3.12**
* **Django 5 + DRF**
* **PostgreSQL**
* **JWT (SimpleJWT)**
* **Djoser** — готовые эндпоинты для регистрации/логина
* **Swagger** — документация API
* **Docker / Docker Compose**

---

## ⚡️ 1. Что нужно установить

* [Python 3.12+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* [Docker](https://www.docker.com/) и **Docker Compose** (если планируется запуск в контейнере)
* (опционально) [PostgreSQL](https://www.postgresql.org/download/) — если запуск без Docker

---

## ⚡️ 2. Клонирование репозитория

```bash
git clone https://github.com/yourusername/alumni.git
cd alumni
```

---

## ⚡️ 3. Настройка окружения

Создайте файл **.env** в корне проекта (рядом с `docker-compose.yml`):

```env
DEBUG=True
SECRET_KEY=super_secret_key
ALLOWED_HOSTS=*

POSTGRES_DB=alumni_db
POSTGRES_USER=alumni_user
POSTGRES_PASSWORD=alumni_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> ⚠️ Для продакшена выстави `DEBUG=False` и придумай **уникальный SECRET\_KEY** и localhost в POSTGRES_HOST поставь.

---

## 🖥 4. Локальный запуск (без Docker)

### Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### Настройка БД

Если работаешь локально, создай базу в PostgreSQL:

```sql
CREATE DATABASE alumni_db;
CREATE USER alumni_user WITH PASSWORD 'alumni_pass';
GRANT ALL PRIVILEGES ON DATABASE alumni_db TO alumni_user;
```
 и поменяй в .env POSTGRES_HOST на localhost
### Миграции и статика

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

### Запуск сервера

```bash
python manage.py runserver
```

API будет доступно на:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐳 5. Запуск через Docker

### Сборка контейнеров

```bash
docker compose build
```

### Запуск

```bash
docker compose up -d
```

### Создание суперпользователя (первый раз)

```bash
docker compose exec web python manage.py createsuperuser
```

После запуска:

* **API** → [http://localhost:8000/api/](http://localhost:8000/api/)
* **Swagger** → [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **Админка** → [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔑 Авторизация

Используется **JWT**:

* Получить токен: `POST /token/`
* Обновить токен: `POST /token/refresh/`

В заголовках запросов нужно указывать:

```
Authorization: Bearer <access_token>
```

---

## 📂 Основные эндпоинты

| Метод | URL               | Описание                        |
| ----- | ----------------- | ------------------------------- |
| POST  | `/auth/users/`    | Регистрация                     |
| POST  | `/token/`         | Получение JWT токена (логин)    |
| POST  | `/token/refresh/` | Обновление access токена        |
| GET   | `/news/`          | Список новостей (доступно всем) |
| POST  | `/feedback/`      | Отправить отзыв (доступно всем) |
| GET   | `/feedback/`      | Список отзывов (только админ)   |

---

## ⚙️ Полезные команды (Docker)

| Команда                        | Действие                        |
| ------------------------------ | ------------------------------- |
| `docker compose logs -f`       | Логи всех контейнеров           |
| `docker compose exec web bash` | Зайти внутрь контейнера Django  |
| `docker compose down`          | Остановить и удалить контейнеры |
| `docker compose down -v`       | + удалить volume (БД)           |

---

## 📝 Примечания

* Для продакшена **обязательно** поменяй `SECRET_KEY` и `POSTGRES_PASSWORD` в `.env`.
* Если нужен автологин после регистрации — фронтенд получает JWT-токен и хранит его (обычно в `HttpOnly` cookie или localStorage).
* Документация Swagger на русском доступна по адресу `/swagger/`.

---


