import threading
import time
from typing import Callable, Iterable, Optional, List


class PeriodicTask:
    def __init__(
            self,
            interval_seconds: int,
            event: Callable,
            event_args: Optional[tuple] = None,
            daemon: bool = True
    ):
        self.event = event
        self.event_args = event_args or ()
        self.interval_seconds = interval_seconds

        self.running = True

        self.thread = threading.Thread(target=self.run, daemon=daemon)

    def run(self):
        while self.running:
            if self.event_args:
                self.event(*self.event_args)
            else:
                self.event()

            time.sleep(self.interval_seconds)

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

