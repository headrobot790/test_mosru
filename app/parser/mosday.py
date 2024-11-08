from datetime import datetime
from typing import List

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import settings
from crud.news import NewsCRUD


async def get_news_text(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), "lxml")
            text = soup.select_one("#saDivCalcMAIN > table > tr > td > main > font > article > font > div:nth-child(1) > p").text

            return text
        else:
            return ""


async def fetch_news(session: aiohttp.ClientSession) -> List[dict] | None:
    random_user_agent = UserAgent().random
    url = settings.parser.url
    news_link = settings.parser.news_link
    headers = {
        "User-Agent": random_user_agent
    }

    async with session.get(url, headers=headers) as response:
        def get_text(element, selector):
            selected = element.select_one(selector)
            return selected.text if selected else ""

        def get_attr(element, selector, attr, prefix=""):
            selected = element.select_one(selector)
            return f"{prefix}{selected.get(attr)}" if selected else ""

        if response.status == 200:
            html = await response.text()
            news_items = []
            soup = BeautifulSoup(html, "lxml")

            #  --- CSS selectors ---
            news = soup.select(
                "body > table:nth-child(2) > tr > td:nth-child(3) > table > tr > td > center > table > tr")
            #  CSS path from parent "news"
            article_selector = "td:nth-child(2) > font > font > a > b"
            img_url_selector = "td:nth-child(1) > a > img"
            link_selector = "td:nth-child(2) > font > font > a"
            news_date_selector = "td:nth-child(2) > font > b"
            #  --- CSS selectors END BLOCK ---

            count_news = len(news) - 1

            for i in range(0, count_news):
                article = get_text(news[i], article_selector)
                img_url = get_attr(news[i], img_url_selector, "src", news_link)
                link = get_attr(news[i], link_selector, "href", news_link)
                body_text = await get_news_text(session, link)

                try:
                   news_date = datetime.strptime(news[i].select_one(news_date_selector).text, "%d.%m.%Y").date()
                except:
                   news_date = None

                news_items.append(
                    {
                        "article": article,
                        "img_url": img_url,
                        "link": link,
                        "body_text": body_text,
                        "news_date": news_date
                    }
                )
            return news_items
        else:
            return []


async def start_parsing() -> None:
    async with aiohttp.ClientSession() as session:
        news = await fetch_news(session)
        for new in news:
            await NewsCRUD.add_record(
                article=new["article"],
                img_url=new["img_url"],
                link=new["link"],
                body_text=new["body_text"],
                news_date=new["news_date"],
            )




