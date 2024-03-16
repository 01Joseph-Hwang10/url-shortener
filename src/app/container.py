from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Object
from peewee import Database, SqliteDatabase
from src.db.model import URL
from src.url_shortener import URLShortenerService
from .config import Config


class Container(DeclarativeContainer):

    # --------------------
    # Config
    # --------------------
    config: Config = Singleton(Config)

    # --------------------
    # Database
    # --------------------
    db: Database = Object(SqliteDatabase("db.sqlite3"))

    # --------------------
    # Models
    # --------------------
    url: URL = Object(URL)

    # --------------------
    # Services
    # --------------------
    url_shortener: URLShortenerService = Singleton(URLShortenerService)
