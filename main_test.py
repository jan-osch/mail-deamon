#!/usr/bin/env python3

import unittest

from main import check_structure


class TestStringMethods(unittest.TestCase):
    def test_should_return_true_for_simple_types(self):
        self.assertTrue(check_structure(str, ''))
        self.assertTrue(check_structure(int, 1))
        self.assertTrue(check_structure(float, 1.1))
        self.assertTrue(check_structure(list, []))
        self.assertTrue(check_structure(dict, {}))

    def test_should_return_false_if_type_does_not_match(self):
        self.assertFalse(check_structure(str, 1))
        self.assertFalse(check_structure(int, '1'))
        self.assertFalse(check_structure(float, 1))
        self.assertFalse(check_structure(list, {}))
        self.assertFalse(check_structure(dict, []))

    def test_tuple_in_schema_indicates_alternative(self):
        self.assertTrue(check_structure((str, int), '1'))
        self.assertTrue(check_structure((str, int), 1))

    def test_should_check_each_element_for_list_types(self):
        self.assertTrue(check_structure([int], []))
        self.assertTrue(check_structure([int], [1, 2, 3]))
        self.assertFalse(check_structure([int], [1, '2', 3]))

    def test_should_work_for_complex_types(self):
        schema = {
            'a': [int]
        }

        data = {
            'a': [1, 2, 3, 4, 5, 6]
        }

        self.assertTrue(check_structure(schema, data))

    def test_should_ignore_additional_keys(self):
        schema = {
            'a': [int]
        }

        data = {
            'a': [],
            'b': 'is_ok'
        }

        self.assertTrue(check_structure(schema, data))


if __name__ == '__main__':
    unittest.main()
