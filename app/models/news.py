from datetime import datetime

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article: Mapped[str] = mapped_column(String, index=True)
    img_url: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String, unique=True)
    body_text: Mapped[str] = mapped_column(String)
    news_date: Mapped[datetime] = mapped_column(Date, nullable=True)
