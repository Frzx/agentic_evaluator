from abc import ABCMeta, abstractmethod
import threading
import logging

class SingletonABCMeta(ABCMeta):

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
        
class BaseLogger(metaclass=SingletonABCMeta):

    @abstractmethod
    def debug(self, message: str): ...
    @abstractmethod
    def info(self, message: str): ...
    @abstractmethod
    def warning(self, message: str): ...
    @abstractmethod
    def error(self, message: str): ...
    @abstractmethod
    def critical(self, message: str): ...

class AppLogger(BaseLogger):

    def __init__(self, name):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.handlers:
            handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")
            formatter = logging.Formatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def debug(self, message): self._logger.debug(message)
    def info(self, message): self._logger.info(message)
    def warning(self, message): self._logger.warning(message)
    def error(self, message): self._logger.error(message)
    def critical(self, message): self._logger.critical(message)