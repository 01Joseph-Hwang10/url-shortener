import abc
from src import models


class URLRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, url: str, key: str) -> models.URL:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_key(self, key: str) -> models.URL | None:
        raise NotImplementedError
