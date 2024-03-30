from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Object, Resource
from peewee import Database, SqliteDatabase
from src.db.model import URL
from src.url_shortener._service import URLShortenerService
from .config import Config


def _database_resource():
    db = SqliteDatabase("db/db.sqlite3")
    db.connect()
    yield db
    db.close()


class Container(DeclarativeContainer):

    # --------------------
    # Config
    # --------------------
    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "src.url_shortener._service",
            "src.url_shortener._router",
        ],
        auto_wire=False,
    )
    config: Singleton[Config] = Singleton(Config)

    # --------------------
    # Database
    # --------------------
    db: Resource[Database] = Resource(_database_resource)

    # --------------------
    # Models
    # --------------------
    url: Object[URL] = Object(URL)

    # --------------------
    # Services
    # --------------------
    url_shortener: Singleton[URLShortenerService] = Singleton(URLShortenerService)
