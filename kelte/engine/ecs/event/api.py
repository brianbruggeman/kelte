from .event import Event
from .queue import EventQueue

event_queue = EventQueue()


def emit(action, entity, data):
    global event_queue
    event = Event(action, entity, data)
    event_queue.put(event)
    print(event_queue)


def next():
    global event_queue
    yield from event_queue.get()
