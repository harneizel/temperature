from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
import asyncio
import datetime

from database import models,requests

#собирает температуру с датчиков
async def get_temp():
    while True:
        try:
            inner_html_code = str(urlopen('http://192.168.217.144').read(), 'utf-8') # айпи датчика в локальной сети
            inner_soup = BeautifulSoup(inner_html_code, "html.parser")
            temp = inner_soup.get_text()[:-1]
            date_time = datetime.datetime.now()
            current_date = datetime.date.today()
            current_time = date_time.strftime("%H:%M:%S")
            await requests.add_temp(current_date, current_time, temp)
            print(f"Дата: {current_date}, время: {current_time}, температура: {temp}")
            sleep(1)
        except:
            print('Датчик недоступен')

