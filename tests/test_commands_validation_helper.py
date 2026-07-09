import unittest
from enums.city import City
from commands.validation_helper import (
    validate_params_count, try_parse_city, try_parse_float, try_parse_int
)

class ValidationHelperShould(unittest.TestCase):

    def test_validate_params_count(self):
        validate_params_count(["A", "B"], 2, "Test")

        with self.assertRaises(ValueError):
            validate_params_count(["A"], 2, "Test")

    def test_try_parse_city_valid(self):
    
        self.assertEqual(try_parse_city("MEL"), City.MEL)
        self.assertEqual(try_parse_city("mel"), City.MEL)
        self.assertEqual(try_parse_city("  MEL  "), City.MEL)

    def test_try_parse_city_invalid(self):
        with self.assertRaises(ValueError):
            try_parse_city("NOT_A_CITY")

    def test_try_parse_float_valid(self):
        self.assertEqual(try_parse_float("12.34"), 12.34)

    def test_try_parse_float_invalid(self):
        with self.assertRaises(ValueError):
            try_parse_float("abc")

    def test_try_parse_int_valid(self):
        self.assertEqual(try_parse_int("42"), 42)

    def test_try_parse_int_invalid(self):
        with self.assertRaises(ValueError):
            try_parse_int("42.5") 