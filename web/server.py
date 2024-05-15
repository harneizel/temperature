from flask import Flask, render_template
import asyncio
from database import models, requests


app = Flask(__name__)

@app.route('/') # отправка текущей темпы на сайт
def get_temp():
    curr_temp = asyncio.run(requests.get_temp())
    print(f'ТЕКУЩАЯ ТЕМПЕРАТУРА {curr_temp}')

    return render_template('index.html', temp=curr_temp)

