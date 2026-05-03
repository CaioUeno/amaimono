import random
from datetime import datetime
from time import sleep
from typing import List

from redis import Redis


class FakeEventTracker:
    def __init__(self, events: List[str], redis_client: Redis):
        self.events = events
        self.redis_client = redis_client

    def track(self):
        while True:
            for event in self.events:
                n_events = random.randint(1, 10)
                key_name = f"{event}:{datetime.now().strftime('%Y%m%d%H%M')}"
                self.redis_client.incrby(key_name, n_events)
                print(f"{event}: registered {n_events} events")
                sleep(1)


if __name__ == "__main__":
    tracker = FakeEventTracker(events=["INIT", "SUCCESS", "ERROR"],
                               redis_client=Redis(host="localhost", port=6379, db=0))
    tracker.track()
