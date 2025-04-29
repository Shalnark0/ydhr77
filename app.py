from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

from models import db, MyData

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('Файл не выбран')
            return redirect(request.url)

        try:
            data = json.load(file)
        except Exception:
            flash('Невозможно прочитать JSON')
            return redirect(request.url)

        if not isinstance(data, list):
            flash('Неверный формат данных: должен быть список объектов')
            return redirect(request.url)

        records = []
        for item in data:
            name = item.get('name')
            date_str = item.get('date')

            if not name or not date_str:
                flash('Ошибка: отсутствуют ключи name или date')
                return redirect(request.url)
            if len(name) >= 50:
                flash(f'Ошибка: слишком длинное имя — {name}')
                return redirect(request.url)
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d_%H:%M')
            except ValueError:
                flash(f'Ошибка: неверный формат даты — {date_str}')
                return redirect(request.url)

            records.append(MyData(name=name, date=dt))

        db.session.add_all(records)
        db.session.commit()
        flash('Файл успешно загружен и сохранён в базу')
        return redirect(url_for('records'))

    return render_template('upload.html')

@app.route('/records')
def records():
    all_records = MyData.query.all()
    return render_template('records.html', records=all_records)

@app.route('/map')
def map_view():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
