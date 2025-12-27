import datetime
from typing import Callable, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    def schedule(self, run_at: datetime, to_run: Callable[[], None]):
        self.scheduler.add_job(to_run, 'date', run_date=run_at)


if __name__ == "__main__":
    import time

    def say_hello():
        print(f"Hello, mother fuc-! Time: {datetime.datetime.now()}")

    sched = Scheduler()
    sched.schedule(datetime.datetime.now().replace(second=datetime.datetime.now().second + 5), say_hello)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sched.scheduler.shutdown()