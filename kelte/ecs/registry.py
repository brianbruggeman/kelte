# Registry requirements
#    Queryable entries by name if name is present
#


class EcsRegistry(type):

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        pass
    #
    # def register(self, entry):
    #         raise ValueError(f'Object "{entry}" must be of type but is {type(entry)}')
    #     self.entries.setdefault(entry.name, {})[entry.id] = entry
    #
    # def unregister(self, entry: T):
    #     if not isinstance(entry, T):
    #         raise ValueError(f'Object "{entry}" must be of type {T} but is {type(entry)}')
    #     return self.entries.get(entry.name, {}).pop(entry.id, None)
