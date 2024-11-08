from sqlalchemy.dialects.postgresql import insert
from database import async_session_maker


class BaseCRUD:
    model = None


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