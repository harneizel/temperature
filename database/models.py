from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SQLALCHEMY_URL = "sqlite+aiosqlite:///db.sqlite3"
engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Temp1(Base):
    __tablename__ = 'temp1'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    temp: Mapped[float] = mapped_column()

class Temp2(Base):
    __tablename__ = 'temp2'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    temp: Mapped[float] = mapped_column()

class Temp3(Base):
    __tablename__ = 'temp3'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    temp: Mapped[float] = mapped_column()




async def on_startup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)