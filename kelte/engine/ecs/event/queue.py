import collections

from .event import Event


class EventQueue:
    @property
    def full(self):
        return len(self.queue) == self.queue.maxlen if self.queue.maxlen else False

    @property
    def empty(self):
        return len(self.queue) == 0

    def consume(self, type=None, **kwds):
        for item in self.get(type=type, **kwds):
            self.queue.remove(item)
            yield item

    def get(self, type=None, **kwds):
        for item in self.queue:
            if type and not isinstance(item, type):
                continue
            if kwds:
                for k, v in kwds.items():
                    if hasattr(item, k) and getattr(item, k) == v:
                        yield item
            else:
                yield item

    def put(self, item):
        if isinstance(item, Event):
            self.queue.append(item)
        else:
            raise TypeError(f"{item!r} is not of type Event")

    def __init__(self):
        self.queue = collections.deque()

    def __iter__(self):
        for item in self.queue:
            yield item

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return f"<{type(self).__name__} count={len(self)}>"
