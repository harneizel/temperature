from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from database.models import async_session, Temp1, Temp2, Temp3



async def get_temps():
    async with async_session() as session:
        result = await session.scalars(select(Temp1))
        return result

# добавляет температуру в базу данных
async def add_temp(number, date, time, temp):
    async with async_session() as session:
        try:
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
async def get_temp():
    async with async_session() as session:
        result = []
        min_id = await session.scalar(func.min(Temp1.id))
        max_id = await session.scalar(func.max(Temp1.id)) #Temp1.date, Temp1.time,
        result.append((await session.execute(select(Temp1.date, Temp1.time).where(Temp1.id == min_id))).one()) #дата время когда темпа начачла собираться
        result.append((await session.execute(select(Temp1.date, Temp1.time).where(Temp1.id == max_id))).one())
        result.append(await session.scalar(select(Temp1.temp).where(Temp1.id == max_id))) #последняя собранная темпа
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