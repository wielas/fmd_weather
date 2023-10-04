import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from sqlalchemy import exc
from weather_app.db import db, City

weather_bp = Blueprint('weather', __name__, url_prefix='/')


@weather_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            new_city = request.form.get('city')

            if new_city:
                new_city_obj = City(name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
        except (exc.IntegrityError, exc.PendingRollbackError):
            error = f"City {new_city} is already registered."

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=591e22f2a995634aa4214bad238cab35'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'temperature': round((int(r['main']['temp']) - 32) * 5 / 9),  # F to C conversion
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('current_weather.html', weather_data=weather_data)


@weather_bp.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'POST':
        print(request.form)
        city_to_delete = request.form.get('delete_city')
        print(f'deleted city {city_to_delete}')

        if city_to_delete:
            city_to_delete_obj = City.query.filter_by(name=city_to_delete).first()

            db.session.delete(city_to_delete_obj)
            db.session.commit()
    return redirect('/')


@weather_bp.route('/air_pollution', methods=['GET', 'POST'])
def air_pollution():
    current_city = ''
    url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=591e22f2a995634aa4214bad238cab35'
    if request.method == 'POST':
        pass

    if current_city:
        cities = City.query.first()

        # city = City.query.filter_by(name=current_city)

