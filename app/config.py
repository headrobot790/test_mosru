from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserConfig(BaseModel):
    url: str = "https://mosday.ru/news/tags.php?metro"
    news_link: str = "https://mosday.ru/news/"


class DatabaseConfig(BaseSettings):
    API_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        database_url = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return database_url

    model_config = SettingsConfigDict(env_file=".env")


class AppConfig(BaseSettings):
    title: str = "News getter"
    docs_url: str = "/docs"
    description: str = "Get news articles for period"
    parser: ParserConfig = ParserConfig()
    db: DatabaseConfig = DatabaseConfig()

settings = AppConfig()
