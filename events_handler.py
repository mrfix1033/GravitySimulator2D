import typing

from events.events_physics import *


class EventsHandler:
    def __init__(self):
        self._registered_events = dict()

    def register(self, event_class: type[Event]):
        self._registered_events[event_class] = list()

    def add_listener(self, event_class: type[Event], listener: typing.Callable[[Event], typing.Any]):
        if event_class not in self._registered_events:
            raise RuntimeError("Event is not registered")
        self._registered_events[event_class].append(listener)

    def call(self, event: Event):
        event_class = type(event)
        if event_class not in self._registered_events:
            raise RuntimeError("Event is not registered")
        for listener in self._registered_events[event_class]:
            listener(event)
