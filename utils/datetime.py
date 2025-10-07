import pytz
from datetime import datetime


def now(tz=pytz.UTC) -> datetime:
    return datetime.now(tz=tz)
