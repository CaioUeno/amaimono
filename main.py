from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Query
from pydantic import BaseModel
from redis import Redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_event_count(self, event_name: str, timestamps: List[datetime]):
        counts = [self.redis_client.get(f"{event_name}:{ts.strftime("%Y%m%d%H%M")}") for ts in timestamps]
        return list(map(lambda x: x if x is not None else 0, counts))


class GroupData(BaseModel):
    name: str
    x: List[str]
    y: List[int]


class TimeSeriesResponse(BaseModel):
    data: List[GroupData]


@app.get(path="/events", response_model=TimeSeriesResponse, status_code=HTTPStatus.OK)
async def get_events(
        names: str = Query(),
        last: int = Query(10),
):
    event_service = EventService(redis_client=Redis(host="localhost", port=6379, db=0))
    now = datetime.now()
    lm = [(now - timedelta(minutes=i)) for i in range(1, last)]
    lm.reverse()

    shared_x = [item.strftime("%Y-%m-%d %H:%M") + ":00" for item in lm]

    data = []
    for name in names.split(","):
        data.append(GroupData(name=name,
                              x=shared_x,
                              y=event_service.get_event_count(event_name=name, timestamps=lm))
                    )

    return TimeSeriesResponse(data=data)
