import requests
import pandas as pd
from requests_ratelimiter import LimiterSession

from config import settings


class ColumnsMismatchException(Exception):
    pass


class JSONPlaceholderAPI:
    session = LimiterSession(per_second=7)
    allowed_columns = ["userId", "title", "body"]

    def handle_csv_userdata(self, df: pd.DataFrame, fake=False) -> list[int]:
        url = settings.jsonplaceholder_url
        result = []
        if not all(df.columns.isin(self.allowed_columns)):
            raise ColumnsMismatchException(
                f"DataFrame columns({list(df.columns)}) should be {self.allowed_columns}"
            )
        for index, row in df.iterrows():
            if not fake:
                r = self.session.post(url, data=row.to_dict())
                if r.status_code == 200:
                    result.append(index)
            else:
                result.append(index)
        return result

JSONPLACEHOLDER_API = JSONPlaceholderAPI()
