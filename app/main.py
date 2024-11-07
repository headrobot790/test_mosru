from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from api.routers.news import router as news_router
from parser.mosday import start_parsing

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(start_parsing, IntervalTrigger(minutes=10), id="news_parser", replace_existing=True)
    scheduler.start()
    print("запускаем приложение")
    yield
    scheduler.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="News getter",
    docs_url="/docs/api",
    description="Get news articles for period",
    debug=True,
)

app.include_router(news_router, prefix="/news")



