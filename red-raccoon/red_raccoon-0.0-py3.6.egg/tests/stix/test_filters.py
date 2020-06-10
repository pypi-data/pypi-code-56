from red_raccoon.stix.filters import Filter

import red_raccoon.stix.filters
import unittest


class FilterTestCases(unittest.TestCase):
    def test_get_generic_filter_eq(self):
        predicate = red_raccoon.stix.filters.get_generic_filter("type", "=", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_generic_filter_in(self):
        predicate = red_raccoon.stix.filters.get_generic_filter("type", "in", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, 'in')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_string_field_filter_eq(self):
        predicate = red_raccoon.stix.filters.get_string_field_filter("type", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_string_field_filter_in(self):
        predicate = red_raccoon.stix.filters.get_string_field_filter("type", ("attack-pattern", "course-of-action"))
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, 'in')
        self.assertEqual(predicate.value, ('attack-pattern', 'course-of-action'))

    def test_get_boolean_field_filter_eq(self):
        predicate = red_raccoon.stix.filters.get_boolean_field_filter("revoked", True)
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'revoked')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, True)

    def test_get_default_filters_for_objects(self):
        predicates = red_raccoon.stix.filters.get_filters_for_objects()
        self.assertIsInstance(predicates, list)
        self.assertEqual(len(predicates), 0)

    def test_get_default_filters_for_relationships(self):
        expected = [
            red_raccoon.stix.filters.get_object_type_filter("relationship")
        ]
        result = red_raccoon.stix.filters.get_filters_for_relationships()
        self.assertEqual(expected, result)
