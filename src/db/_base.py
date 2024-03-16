from peewee import Model, Proxy, Database

_database_proxy = Proxy()


def register_database(database: Database) -> None:
    _database_proxy.initialize(database)


class BaseModel(Model):
    class Meta:
        database = _database_proxy
