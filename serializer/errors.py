class SerializerError(Exception):
    def __init__(self, thing, reason):
        self.thing = thing
        self.reason = reason


class DumpError(SerializerError):
    def __str__(self):
        return f'Could not serialize object: {repr(self.thing)}. {self.reason}'


class LoadError(SerializerError):
    def __str__(self):
        return f'Could not load object: {repr(self.thing)}. {self.reason}'
