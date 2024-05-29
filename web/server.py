from flask import Flask, render_template, request
import asyncio
from database import models, requests
import datetime


app = Flask(__name__)

@app.route('/', methods=["GET"]) # отправка текущей темпы на сайт
def send_temp():
    result = asyncio.run(requests.get_temp())
    print(result)
    curr_temp = result[2]
    date1 = result[0][0]
    time1 = result[0][1]
    date2 = result[1][0]
    time2 = result[1][1]
    print(f'Запрос текщей температуры: {curr_temp}')
    return render_template('index.html', temp=curr_temp, date1=date1, date2=date2, time1=time1, time2=time2)


@app.route('/get-temperature', methods=['POST'])
def get_temp():
    print(request.form)
    sensor_number = int(request.form.get('sensor_number'))
    temp = request.form.get('temp')[:-1]
    vcc = request.form.get('vcc')
    date_time = datetime.datetime.now()
    current_date = datetime.date.today()
    current_time = date_time.strftime("%H:%M")
    await requests.add_temp(sensor_number, current_date, current_time, temp)
    print(f"Номер датчика: {sensor_number}, дата: {current_date}, время: {current_time}, температура: {temp}, вольтаж: {vcc} В")
    return "Data received successfully"

@app.route('/get-datetime', methods=['GET', 'POST'])
def get_datetime():
    data = request.form
    first_date, first_time, second_date, second_time = data['first_date'], data['first_time'], data['second_date'], data['second_time']
    return 'ok'