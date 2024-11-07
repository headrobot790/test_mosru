from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SNewsResponse(BaseModel):
    article: str
    img_url: str
    link: str
    body_text: str
    news_date: datetime

    model_config = ConfigDict(from_attributes=True)