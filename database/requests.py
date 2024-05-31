from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from database.models import async_session, Temp1, Temp2, Temp3
import datetime


async def get_temps():
    async with async_session() as session:
        result = await session.scalars(select(Temp1))
        return result

# добавляет температуру в базу данных
async def add_temp(number, date, time, temp):
    async with async_session() as session:
        try: # выбор таблицы в зависимости от номера датчика
            if number == 1:
                temp = Temp1(date=date, time=time, temp=temp)
            elif number == 2:
                temp = Temp2(date=date, time=time, temp=temp)
            elif number == 3:
                temp = Temp3(date=date, time=time, temp=temp)
            session.add(temp)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

# забирает последнюю добавленную температуру из базы данных
async def get_data():
    async with async_session() as session:
        def datetime_format(ind): #форматирует дату и время чтобы можно было сравнивать
            dt = datetime.datetime(int(res[ind][0][0:4]), int(res[ind][0][5:7]), int(res[ind][0][8:]),
                                   int(res[ind][1][0:2]), int(res[ind][1][3:]))
            return dt
        res = {} #d-датчик, первое число номер датчика второе первая или вторая крайние даты
        res['d1-1'] = (await session.execute(
            select(Temp1.date, Temp1.time).where(Temp1.id == await session.scalar(func.min(Temp1.id))))).one()
        res['d1-2'] = (await session.execute(
            select(Temp1.date, Temp1.time).where(Temp1.id == await session.scalar(func.max(Temp1.id))))).one()
        res['d2-1'] = (await session.execute(
            select(Temp2.date, Temp2.time).where(Temp2.id == await session.scalar(func.min(Temp2.id))))).one()
        res['d2-2'] = (await session.execute(
            select(Temp2.date, Temp2.time).where(Temp2.id == await session.scalar(func.max(Temp2.id))))).one()
        res['d3-1'] = (await session.execute(
            select(Temp3.date, Temp3.time).where(Temp3.id == await session.scalar(func.min(Temp3.id))))).one()
        res['d3-2'] = (await session.execute(
            select(Temp3.date, Temp3.time).where(Temp3.id == await session.scalar(func.max(Temp3.id))))).one()

        result = {}
        dt1 = datetime_format('d1-1') # форматируем чтобы найти промежуток в котором для всех термометров есть данные
        dt2 = datetime_format('d2-1')
        dt3 = datetime_format('d3-1')
        dt4 = datetime_format('d1-2')
        dt5 = datetime_format('d2-2')
        dt6 = datetime_format('d3-2')
        datetime1 = max(dt1, dt2, dt3)
        datetime2= min(dt4, dt5, dt6)
        if datetime2>datetime1:
            result['status']='coincid'
        else:
            result['status']='not_coincid'
        result['datetime1'] = datetime1.strftime("%Y-%m-%d %H:%M")
        result['datetime2'] = datetime2.strftime("%Y-%m-%d %H:%M")
        result['temp1'] = (await session.scalars(select(Temp1.temp).where(
            Temp1.id == await session.scalar(func.max(Temp1.id))))).one() #последняя собранная темпа на 1
        result['temp2'] = (await session.scalars(select(Temp2.temp).where(
            Temp2.id == await session.scalar(func.max(Temp2.id))))).one()  # последняя собранная темпа на 1
        result['temp3'] = (await session.scalars(select(Temp3.temp).where(
            Temp3.id == await session.scalar(func.max(Temp3.id))))).one()  # последняя собранная темпа на 1
        print(result)
        return result



'''
async def update_user(user_id: int, **kwargs):
    async with async_session() as session:
        await session.execute(update(User).where(User.user_id == user_id).values(**kwargs))
        await session.commit()


async def delete_user(user_id: int):
    async with async_session() as session:
        await session.execute(delete(User).where(User.user_id == user_id))
        await session.commit()
'''