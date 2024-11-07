from crud.base import BaseCRUD
from models.news import News


class NewsCRUD(BaseCRUD):
    model = News
