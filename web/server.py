from flask import Flask, render_template, request
import asyncio
from database import models, requests
import datetime


app = Flask(__name__)

@app.route('/', methods=["GET"]) # отправка текущей темпы на сайт
def send_temp():
    data = asyncio.run(requests.get_data())
    print(data)
    date1, date2 = data['datetime1'], data['datetime2']
    temp1, temp2, temp3 = data['temp1'], data['temp2'], data['temp3']
    print(f'Запрос текщей температуры: {temp1, temp2, temp3}')
    return render_template('index.html', temp1=temp1, temp2=temp2, temp3=temp3, date1=date1, date2=date2)

# обработка темпы от датчика
@app.route('/get-temperature', methods=['POST'])
def get_temp():
    print(request.form)
    sensor_number = int(request.form.get('sensor_number'))
    temp = request.form.get('temp')[:-1]
    vcc = request.form.get('vcc')
    date_time = datetime.datetime.now()
    current_date = datetime.date.today()
    current_time = date_time.strftime("%H:%M")
    asyncio.run(requests.add_temp(sensor_number, current_date, current_time, temp))
    print(f"Номер датчика: {sensor_number}, дата: {current_date}, время: {current_time}, температура: {temp}, вольтаж: {vcc} В")
    return "Data received successfully"

@app.route('/get-datetime', methods=['GET', 'POST'])
def get_datetime():
    cl_data = request.form #получение client data, то что клиент ввел на сайте
    data = asyncio.run(requests.get_data()) # данные из базы данных
    print(f"Данные клиента: {cl_data}")
    print(f"Данные из бд: {data}")
    first_date, first_time, second_date, second_time = cl_data['first_date'], cl_data['first_time'], cl_data['second_date'], cl_data['second_time']
    if first_date or first_time or second_date or second_time == None:
        print(first_date,first_time,second_date,second_time)
        return "вы заполнили не все поля"
    date1, date2 = data['datetime1'], data['datetime2']
    temp1, temp2, temp3 = data['temp1'], data['temp2'], data['temp3']

    return render_template('chart.html', temp1=temp1, temp2=temp2, temp3=temp3, date1=date1, date2=date2)