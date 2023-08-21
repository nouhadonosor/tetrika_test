from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jsonplaceholder_url: str = "https://jsonplaceholder.typicode.com/posts"
    celery_broker_url: str
    celery_result_backend: str
    tempfiles_dir: str = "tempfiles"
    result_dir: str = "resfiles"


settings = Settings()
