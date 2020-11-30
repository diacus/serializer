from .serializer import Serializer as __Serializer

__serializer = __Serializer()


def load(thing):
    """
    A basic example to send a message to the outside

    Usage:

    >>> import serializer
    >>> from package.module import Klass
    >>> from outside_world import send_message
    >>> original = Klass()
    >>> serialized_klass_instance = serializer.dump(original)
    >>> send_message(serialized_klass_instance)
    """
    return __serializer.load(thing)


def dump(thing):
    """
    A basic example to receive a message from the outside

    Usage:

    >>> import serializer
    >>> from outside_world import receive_message
    >>> serialized_klass_instance = receive_message
    >>> reconstructed_message = serializer.load(serialized_klass_instance)
    """
    return __serializer.dump(thing)
