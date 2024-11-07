from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from database import async_session_maker


class BaseCRUD:
    model = None

    @classmethod
    async def find_news_for_last_days(cls, days: int):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns)
                .where(cls.model.news_date >= datetime.now() - timedelta(days=days)))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_record(cls, **data):
        async with async_session_maker() as session:
            query = (
                insert(cls.model)
                .values(**data)
                .on_conflict_do_update(
                    index_elements=['link'],
                    set_=data
                )
            )
            await session.execute(query)
            await session.commit()