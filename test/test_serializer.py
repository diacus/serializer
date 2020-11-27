import unittest

import serializer
from serializer.errors import DumpError, LoadError


class TheTestClass:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class TestMain(unittest.TestCase):
    maxDiff = None

    def test_dump_success(self):
        original = TheTestClass()
        original.value = "The test value"

        serialized = serializer.dump(original)

        self.assertDictEqual(
            {
                '__module__': 'test.test_serializer',
                '__name__': 'TheTestClass',
                '__state__': {'_value': 'The test value'}
            },
            serialized
        )

    def test_dump_fails_by_recursion(self):
        original = TheTestClass()
        original.value = original

        with self.assertRaises(DumpError):
            serializer.dump(original)

    def test_load_success(self):
        raw_data = {
            '__module__': 'test.test_serializer',
            '__name__': 'TheTestClass',
            '__state__': {'_value': 'The test value'}
        }

        loaded_object = serializer.load(raw_data)

        self.assertIsInstance(loaded_object, TheTestClass)
        self.assertEqual('The test value', loaded_object.value)

    def test_load_fail_with_import_error(self):
        raw_data = {
            '__module__': 'test.other_test_serializer',
            '__name__': 'TheTestClass',
            '__state__': {'_value': 'The test value'}
        }
        expected_message = (
            "Could not load object: {'__module__': "
            "'test.other_test_serializer', '__name__': 'TheTestClass', "
            "'__state__': {'_value': 'The test value'}}. Could not import "
            "module test.other_test_serializer"
        )

        with self.assertRaises(LoadError) as failure:
            serializer.load(raw_data)

        self.assertEqual(expected_message, str(failure.exception))

    def test_load_fail_with_class_not_found(self):
        raw_data = {
            '__module__': 'test.test_serializer',
            '__name__': 'TheFakeTestClass',
            '__state__': {'_value': 'The test value'}
        }
        expected_message = (
            "Could not load object: {'__module__': 'test.test_serializer', "
            "'__name__': 'TheFakeTestClass', '__state__': {'_value': 'The "
            "test value'}}. Module test.test_serializer does not have class "
            "TheFakeTestClass"
        )

        with self.assertRaises(LoadError) as failure:
            serializer.load(raw_data)

        self.assertEqual(expected_message, str(failure.exception))

    def test_load_fail_with_invalid_dict(self):
        raw_data = {
            '__state__': 'Whatever'
        }

        expected_message = (
            "Could not load object: {'__state__': 'Whatever'}. __module__ is "
            "missing"
        )

        with self.assertRaises(LoadError) as failure:
            serializer.load(raw_data)

        self.assertEqual(expected_message, str(failure.exception))
