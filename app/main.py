from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from api.news import router as news_router
from config import settings
from parser.mosday import start_parsing

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_parsing()
    scheduler.add_job(start_parsing, IntervalTrigger(minutes=10), id="news_parser", replace_existing=True)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title=settings.title,
    docs_url=settings.docs_url,
    description=settings.description,
    debug=True,
)

app.include_router(news_router)
