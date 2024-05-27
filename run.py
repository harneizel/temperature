import asyncio
from collector import get_temp
from database.models import on_startup_database
from web.server import app
from threading import Thread

if __name__ == '__main__':
    try:
        asyncio.run(on_startup_database()) #подключение к бд
        #thread1 = Thread(target=asyncio.run, args=(get_temp(),))
        #thread1.start() # запуск сбора температуры
        app.run(host='192.168.254.184',port=5000, debug=True) # запуск сайта
    except:
        print("Завершение работы")