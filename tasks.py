import os

import pandas as pd

from worker import celery_app
from jsonplaceholder_api import JSONPLACEHOLDER_API
from config import settings
from redis_api import REDIS_API


@celery_app.task(bind=True, name="handle_csv_userdata")
def handle_csv_userdata(self, filename):
    self_id = self.request.id or "eager"
    REDIS_API.set_key("tasks:status", self_id, "started")
    respath = settings.result_dir + "/" + filename.split("/")[-1] + ".csv"
    res_f = open(respath, "a")
    headers = True
    with open(filename, "r") as f:
        for i, chunk in enumerate(pd.read_csv(f, chunksize=500, on_bad_lines="skip")):
            print(f"Chunk {i}")
            cur_res = JSONPLACEHOLDER_API.handle_csv_userdata(chunk, fake=False)
            if isinstance(cur_res, list):
                filtered = chunk.loc[cur_res]
                filtered.to_csv(res_f, header=headers)
                headers = False
    os.remove(filename)
    REDIS_API.set_key("tasks:status", self_id, "done")
