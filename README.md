## ⚙️ Установка и запуск (Ubuntu 22.04+)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Shalnark0/ydhr77.git
cd ydhr77
```
### 2. Установить зависимости
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Установить и настроить PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```
Создать базу данных и пользователя:
```bash
sudo -u postgres psql
```
Внутри psql:
```bash
CREATE DATABASE geoapp;
CREATE USER geo_user WITH PASSWORD 'geo_pass';
GRANT ALL PRIVILEGES ON DATABASE geoapp TO geo_user;
\q
```
### 4. Настроить подключение к базе данных
В файле app.py отредактируй строку:
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://geo_user:geo_pass@localhost/geoapp'
```
### 5. Инициализировать базу
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```
## 🚀 Запуск приложения через Gunicorn
```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```
## 🌐 Настройка Nginx

### 1. Установить Nginx
```bash
sudo apt install nginx
```
Пример конфигурации /etc/nginx/sites-available/geoapp

```bash
sudo nano /etc/nginx/sites-available/geoapp
```
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    error_log /var/log/nginx/geoapp_error.log;
    access_log /var/log/nginx/geoapp_access.log;
}
```

### 2. Активировать конфигурацию
```bash
sudo ln -s /etc/nginx/sites-available/geoapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```