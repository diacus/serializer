class SerializerError(Exception):
    """Base serializer error"""
    def __init__(self, thing, reason):
        self.thing = thing
        self.reason = reason


class DumpError(SerializerError):
    """
    If the serializer could not transform its imput into a serialized dict
    """
    def __str__(self):
        return f'Could not serialize object: {repr(self.thing)}. {self.reason}'


class LoadError(SerializerError):
    """
    If the serializer could not transform serialized input into a Python object
    """
    def __str__(self):
        return f'Could not load object: {repr(self.thing)}. {self.reason}'
