from os import environ
from datetime import time, timezone, timedelta

TOKEN=environ['GOAT_API_TOKEN']
WHEN_START_POLL=time(22, 00, tzinfo=timezone(timedelta(hours=1)))
WHEN_STOP_POLL=time(23, 59, tzinfo=timezone(timedelta(hours=1)))