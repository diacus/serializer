import sys

from collections import Iterable
from datetime import datetime, timezone
from enum import Enum

from .errors import DumpError, LoadError


def is_iterable(thing):
    return isinstance(thing, Iterable) and not isinstance(thing, str)


class Serializer:
    def _copy_state(self, thing):
        return {
            name: self.dump(value) for name, value in thing.items()
        }

    def _get_klass(self, thing):
        if '__module__' not in thing:
            raise LoadError(thing, '__module__ is missing')

        if '__name__' not in thing:
            raise LoadError(thing, '__name__ is missing')

        module = thing['__module__']
        name = thing['__name__']

        if module not in sys.modules:
            try:
                __import__(module)
            except ModuleNotFoundError:
                raise LoadError(thing, f'Could not import module {module}')

        if not hasattr(sys.modules[module], name):
            raise LoadError(
                thing,
                f'Module {module} does not have class {name}'
            )

        return getattr(sys.modules[module], name)

    def _load_state(self, thing):
        if not isinstance(thing['__state__'], dict):
            raise LoadError(thing, '__state__ must be a dict')

        return {
            name: self.load(value)
            for name, value in thing['__state__'].items()
        }

    def dump(self, thing):
        try:
            if isinstance(thing, Enum):
                klass = type(thing)
                return {
                    '__module__': klass.__module__,
                    '__name__': klass.__name__,
                    '__enum__': thing.value
                }

            if isinstance(thing, datetime):
                return {
                    '__timestamp__': thing.astimezone(timezone.utc).timestamp()
                }

            if hasattr(thing, '__dict__'):
                klass = type(thing)
                return {
                    '__module__': klass.__module__,
                    '__name__': klass.__name__,
                    '__state__': self._copy_state(vars(thing))
                }

            if isinstance(thing, dict):
                return self._copy_state(thing)

            if is_iterable(thing):
                return [self.dump(item) for item in thing]

            return thing
        except RecursionError as error:
            raise DumpError(thing, error)

    def load(self, thing):
        try:
            if not is_iterable(thing):
                return thing

            if isinstance(thing, list):
                return [self.load(item) for item in thing]

            if '__timestamp__' in thing:
                return datetime.fromtimestamp(
                    thing['__timestamp__'],
                    timezone.utc
                )

            if '__enum__' in thing:
                klass = self._get_klass(thing)
                return klass(thing['__enum__'])

            if '__state__' not in thing:
                return {
                    name: self.load(value) for name, value in thing.items()
                }

            klass = self._get_klass(thing)
            state = self._load_state(thing)

            instance = klass.__new__(klass)
            instance.__dict__.update(state)

            return instance

        except RecursionError as error:
            raise error
