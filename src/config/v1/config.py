from pydantic_settings import BaseSettings

class Configuration(BaseSettings):
    @property
    def database(self):
        return "sqlite:///app.db"