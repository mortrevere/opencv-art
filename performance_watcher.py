from collections import deque


class PerformanceWatcher:
    def __init__(self, buffer_size):
        self.observations = deque([0 for _ in range(buffer_size)])

    def observe(self, time):
        self.observations.pop()
        self.observations.appendleft(time)

    def get_time(self):
        return sum(self.observations) / len(self.observations)

    def get_fps(self):
        if self.get_time():
            return 1 / self.get_time()
        else:
            return 0
