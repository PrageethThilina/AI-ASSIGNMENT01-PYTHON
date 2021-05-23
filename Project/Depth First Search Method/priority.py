import heapq
import itertools

# Create a priority queue
class PQ:

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = -1
        self.counter = itertools.count()
        self.size = 0

    #function to pop an object out of the queue
    def pop(self):
        while len(self.pq) > 0:
            priority,count,task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task.hash()]
                self.size -= 1
                return task
        return KeyError("Pop from an empty priority queue",str(self.size),str(self.pq))
