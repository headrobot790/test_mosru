from datetime import datetime, timedelta

from crud.base import BaseCRUD
from database import async_session_maker
from models.news import News
from sqlalchemy import select

class NewsCRUD(BaseCRUD):
    model = News

    @classmethod
    async def find_news_for_last_days(cls, days: int):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns)
                .where(cls.model.news_date >= datetime.now() - timedelta(days=days)))
            result = await session.execute(query)
            return result.mappings().all()