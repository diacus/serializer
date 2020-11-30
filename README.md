# Serialize

Transforms the state of arbitrary objects into Python dictionaries, including
metadata describing how to reconstruct the original objects.

## Install

```sh
pip3 install serialize
```

## Usage

1. Import the module
1. To serialize an object use the `dump()` funtion.
1. To reconstruct a serialized dictionary use the `load()` function.

```python
>>> from pprint import pprint
>>> import serialze
>>> class Foo:
    	def __init__(self):
    		self.list = [1, 2, 3, 4]
    		self.dict = {'one': 1, 'two': 2}
>>> instace = Foo()
>>> serialized_instance = serializer.dump(instance)
>>> pprint(serialized_instance)
{'__module__': '__main__',
 '__name__': 'Foo',
 '__state__': {'dict': {'one': 1, 'two': 2}, 'list': [1, 2, 3, 4]}}
>>> reconstructed_instance = serializer.load(serialized_instance)
>>> reconstructed_instance.list
[1, 2, 3, 4]

>>> reconstructed_instance.dict
{'one': 1, 'two': 2}

>>>
```

