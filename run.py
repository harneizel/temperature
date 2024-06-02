import asyncio
from database.models import on_startup_database
from web.server import app
from threading import Thread

if __name__ == '__main__':
    try:
        asyncio.run(on_startup_database()) #подключение к бд
        app.run(host='192.168.254.184',port=5000, debug=True) # запуск сайта
    except:
        print("Завершение работы")