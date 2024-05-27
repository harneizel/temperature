from flask import Flask, render_template, request
import asyncio
from database import models, requests
import datetime


app = Flask(__name__)

@app.route('/') # отправка текущей темпы на сайт
def send_temp():
    curr_temp = asyncio.run(requests.get_temp())
    print(f'ТЕКУЩАЯ ТЕМПЕРАТУРА {curr_temp}')

    return render_template('index.html', temp=curr_temp)

@app.route('/get-temperature')
def get_temp():
    temp = request.args.get('temperature')
    vcc = request.args.get("vcc")
    date_time = datetime.datetime.now()
    current_date = datetime.date.today()
    current_time = date_time.strftime("%H:%M:%S")
    await requests.add_temp(current_date, current_time, temp)
    print(f"Дата: {current_date}, время: {current_time}, температура: {temp}, вольтаж: {vcc}В")
#