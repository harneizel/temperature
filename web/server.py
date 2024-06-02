from flask import Flask, render_template, request, redirect, url_for, flash
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

# получение данных для аналитики
@app.route('/get-datetime', methods=['GET', 'POST'])
def get_datetime():
    cl_data = request.form #получение client data, то что клиент ввел на сайте
    #data = asyncio.run(requests.get_data()) # данные из базы данных
    print(f"Данные клиента: {cl_data}")
    #print(f"Данные из бд: {data}")
    first_date, first_time, second_date, second_time, sensor = cl_data['first_date'], cl_data['first_time'], cl_data['second_date'], cl_data['second_time'], cl_data['sensor']
    if first_date == '' or first_time == '' or second_date == '' or second_time == '':
        print('Не все поля заполнены')#return "вы заполнили не все поля"

    #date1, date2, status = data['datetime1'], data['datetime2'], data['status']
    #temp1, temp2, temp3 = data['temp1'], data['temp2'], data['temp3']
    if sensor=="all_sensors":
        print('all_sensors')
    else:
        date, time, temp = asyncio.run(requests.get_temps(
            sensor, first_date, first_time, second_date, second_time)) #получение данных для диапазона
        print(time)
        print(temp)
        with open('./web/templates/chart_one.html', 'r') as f:
            html = f.read()
            f.close()
        return render_template('chart_one.html', dtime=time, temp=temp, n=sensor[4])
        #return html%(time, temp, sensor[4])

    #return render_template('chart_all.html', temp1=temp1, temp2=temp2, temp3=temp3, date1=date1, date2=date2)