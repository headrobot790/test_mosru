from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from crud.news import NewsCRUD


async def get_news_text(session, url):
    async with session.get(url) as response:
        print(f"Fetching {url}")
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), "lxml")
            text = soup.select_one("#saDivCalcMAIN > table > tr > td > main > font > article > font > div:nth-child(1) > p").text

            return text
        else:
            return None


async def fetch_news(session):
    url = "https://mosday.ru/news/tags.php?metro"
    partlink = f"https://mosday.ru/news/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    async with session.get(url, headers=HEADERS) as response:
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
                try:
                    article = news[i].select_one(article_selector).text
                except:
                    article = ""

                try:
                    img_url = partlink + news[i].select_one(img_url_selector).get("src")
                except:
                    img_url = ""

                try:
                    link = partlink + news[i].select_one(link_selector).get("href")
                except:
                    link = ""

                try:
                    body_text = await get_news_text(session, link)

                except:
                    body_text = ""

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
            print(f"[{datetime.now()}] Ошибка при получении данных: {response.status}")
            return []


async def start_parsing():
    print("__start_parsing: Запускаем парсинг новостей...")
    async with aiohttp.ClientSession() as session:
        news = await fetch_news(session)
        print(f"[{datetime.now()}] Найдено {len(news)} новостей")
        for new in news:
            await NewsCRUD.add_record(
                article=new["article"],
                img_url=new["img_url"],
                link=new["link"],
                body_text=new["body_text"],
                news_date=new["news_date"],
            )




