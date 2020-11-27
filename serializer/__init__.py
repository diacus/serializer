from .serializer import Serializer as __Serializer

__serializer = __Serializer()


def load(thing):
    return __serializer.load(thing)


def dump(thing):
    return __serializer.dump(thing)
