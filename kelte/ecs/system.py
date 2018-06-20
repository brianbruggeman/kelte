from abc import ABCMeta


class System(metaclass=ABCMeta):
    """Behavior control for components and entities"""

    def update(self, ticks=None):
        """Updates components and entities based on a set of rules
        defined by this method.

        Args:
            ticks (int): Number of ticks since last called
        """
        raise NotImplementedError('.update method must be implemented by subclass')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{type(self).__name__}(name={self.name}, components={self.components})'
