import uuid


class EcsIdentifierDescriptor:
    def __get__(self, instance, owner):
        instance.__dict__.setdefault(self._id_name, uuid.uuid4())
        return instance.__dict__[self._id_name]

    def __set__(self, instance, value):
        value = instance.__dict__[self._id_name]
        value = value.hex if isinstance(value, uuid.UUID) else value
        return value

    def __set_name__(self, owner, name):
        self._id_name = name
