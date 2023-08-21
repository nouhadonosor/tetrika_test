import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router
from config import settings


app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.on_event('startup')
def init():
    if not os.path.exists(settings.tempfiles_dir):
        os.mkdir("./" + settings.tempfiles_dir)

    if not os.path.exists(settings.result_dir):
        os.mkdir("./" + settings.result_dir)
