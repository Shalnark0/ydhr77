## ⚙️ Установка и запуск (Ubuntu 22.04+)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Shalnark0/ydhr77.git
cd ydhr77
2. Установить зависимости

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Установить и настроить PostgreSQL

sudo apt update
sudo apt install postgresql postgresql-contrib
Создать базу данных и пользователя:

sudo -u postgres psql
Внутри psql:

CREATE DATABASE geoapp;
CREATE USER geo_user WITH PASSWORD 'geo_pass';
GRANT ALL PRIVILEGES ON DATABASE geoapp TO geo_user;
\q
4. Настроить подключение к базе данных
В файле app.py отредактируй строку:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://geo_user:geo_pass@localhost/geoapp'
5. Инициализировать базу

flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
## 🚀 Запуск приложения через Gunicorn

gunicorn -w 4 -b 127.0.0.1:8000 app:app
## 🌐 Настройка Nginx
Установить Nginx

sudo apt install nginx
Пример конфигурации /etc/nginx/sites-available/geoapp
nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
        proxy_redirect off;
    }

    location /static/ {
        alias /home/YOUR_USER/ydhr77/static/;
    }
}
Замени YOUR_USER на имя своего пользователя.

Активировать конфигурацию
sudo ln -s /etc/nginx/sites-available/geoapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx