class Queue:

    def __init__(self):
        self.entries = []

    def append(self, obj):
        self.entries.append(obj)

    def pop(self):
        return self.entries.pop()

    def __iter__(self):
        yield from self.entries

    def find(self, **attributes):
        for entry in self.entries:
            for attr_name, attr_value in attributes.items():
                if getattr(entry, attr_name, None) != attr_value:
                    break
                return entry
