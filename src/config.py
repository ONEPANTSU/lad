import os

from dotenv import load_dotenv


class Config:
    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str

    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)
        self.__set_db()

    def __set_db(self) -> None:
        self.driver = os.environ.get("DB_DRIVER")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.name = os.environ.get("DB_NAME")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASSWORD")


config = Config()
