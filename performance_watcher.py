#from collections import deque


class PerformanceWatcher:
    def __init__(self, buffer_size):
        #self.observations = deque([0 for _ in range(buffer_size)])
        self.buffer_size = buffer_size
        self.observations = [0]*self.buffer_size
        self.i = 0
    def observe(self, time):
        #self.observations.pop()
        #self.observations.appendleft(time)
        self.observations[self.i%self.buffer_size] = time
        self.i += 1
    def get_time(self):
        return sum(self.observations) / len(self.observations)

    def get_fps(self):
        if self.get_time():
            return 1 / self.get_time()
        else:
            return 0
