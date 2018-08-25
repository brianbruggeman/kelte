import abc
import queue


class System(metaclass=abc.ABCMeta):
    """Behavior control for components and entities"""

    @property
    def events(self):
        event = self.event_queue.get(block=False)
        yield event
        self.event_queue.task_done()
        self.counter -= 1

    def add_event(self, event, weight=0):
        self.event_queue.put_nowait((weight, event))
        self.counter += 1

    def update(self, ticks=None):
        """Updates components and entities based on a set of rules
        defined by this method.

        Args:
            ticks (int): Number of ticks since last called
        """
        raise NotImplementedError(".update method must be implemented by subclass")

    def __init__(self, name):
        self.name = name
        self.event_queue = queue.PriorityQueue()
        self.counter = 0

    def __len__(self):
        return self.counter

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name}, components={self.components})"
