from stix2 import Filter

import red_raccoon.integrations.stix.filters
import unittest


class FilterTestCases(unittest.TestCase):
    def test_get_filter_eq(self):
        predicate = red_raccoon.integrations.stix.filters.get_filter("type", "=", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_filter_in(self):
        predicate = red_raccoon.integrations.stix.filters.get_filter("type", "in", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, 'in')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_string_filter_eq(self):
        predicate = red_raccoon.integrations.stix.filters.get_string_filter("type", "attack-pattern")
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, 'attack-pattern')

    def test_get_string_filter_in(self):
        predicate = red_raccoon.integrations.stix.filters.get_string_filter("type", ("attack-pattern", "course-of-action"))
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'type')
        self.assertEqual(predicate.op, 'in')
        self.assertEqual(predicate.value, ('attack-pattern', 'course-of-action'))

    def test_get_boolean_filter_eq(self):
        predicate = red_raccoon.integrations.stix.filters.get_boolean_filter("revoked", True)
        self.assertIsInstance(predicate, Filter)
        self.assertEqual(predicate.property, 'revoked')
        self.assertEqual(predicate.op, '=')
        self.assertEqual(predicate.value, True)

    def test_get_default_filters_for_object(self):
        predicates = red_raccoon.integrations.stix.filters.get_filters_for_object()
        self.assertIsInstance(predicates, list)
        self.assertEqual(len(predicates), 0)

    def test_get_default_filters_for_objects(self):
        predicates = red_raccoon.integrations.stix.filters.get_filters_for_objects()
        self.assertIsInstance(predicates, list)
        self.assertEqual(len(predicates), 0)

    def test_get_default_filters_for_relationships(self):
        expected = [red_raccoon.integrations.stix.filters.get_object_type_filter("relationship")]
        result = red_raccoon.integrations.stix.filters.get_filters_for_relationships()
        self.assertEqual(expected, result)

    def test_get_list_of_properties_from_filters(self):
        filters = red_raccoon.integrations.stix.filters.get_filters_for_object(
            object_types=['attack-pattern'],
            object_external_id='S0002',
        )
        expected = ['external_references.external_id', 'type']
        result = red_raccoon.integrations.stix.filters.get_list_of_properties_from_filters(filters)
        self.assertEqual(expected, result)

    def test_get_list_of_human_readable_filters(self):
        filters = red_raccoon.integrations.stix.filters.get_filters_for_object(
            object_types=['attack-pattern'],
            object_external_id='S0002',
        )
        expected = [
            "'external_references.external_id = S0002'",
            "'type = attack-pattern'",
        ]
        result = red_raccoon.integrations.stix.filters.get_list_of_human_readable_filters(filters)
        self.assertEqual(expected, result)
