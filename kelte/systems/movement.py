from kelte.engine.ecs import System


class Movement(System):

    @property
    def events(self):
        events = []

        return events

    def update(self, ticks=1):
        for event in self.events:
