from typing import List

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from crud.news import NewsCRUD
from schemas.news import SNewsResponse

router = APIRouter(prefix="/metro", tags=["news"])


@router.get("/metro", response_model=List[SNewsResponse])
async def get_metro_news(day: int = Query(default=5, ge=1, le=360)) -> JSONResponse:
    news = await NewsCRUD.find_news_for_last_days(day)
    return news
