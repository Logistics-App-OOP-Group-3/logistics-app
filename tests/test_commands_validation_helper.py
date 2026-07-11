import unittest
from unittest.mock import MagicMock, patch
from enums.city import City
import commands.validation_helper as vh
from datetime import datetime
from commands.validation_helper import (
    validate_params_count, try_parse_city, try_parse_date_time, try_parse_float, try_parse_int
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
            

class TryParseDateTime_Should(unittest.TestCase):
    
    def setUp(self):
        
        # Arrange
        self._datetime_patcher = patch('commands.validation_helper.datetime')
        self.mock_datetime = self._datetime_patcher.start()
        self.addCleanup(self._datetime_patcher.stop)
        
        # Keep real strptime behavior; only now() is faked per-test.
        self.mock_datetime.strptime = datetime.strptime
        
    def _set_now(self, *args):
        self.mock_datetime.now.return_value = datetime(*args)
        
    def test_parses_different_ordinal_suffixes(self):

        # Arrange
        self._set_now(2025, 1, 1, 0, 0)
        
        # Act, Assert
        self.assertEqual(
            vh.try_parse_date_time("Jan-1st-09:30h"),
            datetime(2025, 1, 1, 9, 30)
        )
        self.assertEqual(
            vh.try_parse_date_time("Jan-2nd-09:30h"),
            datetime(2025, 1, 2, 9, 30)
        )
        self.assertEqual(
            vh.try_parse_date_time("Jan-3rd-09:30h"),
            datetime(2025, 1, 3, 9, 30)
        )
        self.assertEqual(
            vh.try_parse_date_time("Jan-4th-09:30h"),
            datetime(2025, 1, 4, 9, 30)
        )
        
    def test_is_case_insensitive_for_suffix(self):
        
        # Arrange
        self._set_now(2025, 9, 1, 0, 0)

        # Act
        result = vh.try_parse_date_time("Sep-12TH-06:00h")

        # Assert
        self.assertEqual(result, datetime(2025, 9, 12, 6, 0))

    def test_uses_current_year_when_not_provided(self):
        
        # Arrange
        self._set_now(2030, 3, 1, 0, 0)

        # Act
        result = vh.try_parse_date_time("Mar-15th-10:00h")

        # Assert
        self.assertEqual(result.year, 2030)
        
    def test_parses_without_ordinal_suffix(self):
        
        # Arrange
        self._set_now(2025, 9, 1, 0, 0)

        # Act
        result = vh.try_parse_date_time("Sep-12-06:00h")

        # Assert
        self.assertEqual(result, datetime(2025, 9, 12, 6, 0))
        
    def test_raises_when_date_is_in_the_past(self):
        
        # Arrange
        self._set_now(2025, 9, 15, 0, 0)

        # Act, Assert       
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Sep-12th-06:00h")
            
    def test_allows_future_date_same_year(self):
        
        # Arrange
        self._set_now(2025, 9, 1, 0, 0)

        # Act
        result = vh.try_parse_date_time("Sep-12th-06:00h")

        # Assert
        self.assertEqual(result, datetime(2025, 9, 12, 6, 0))

    def test_raises_when_same_day_but_earlier_time(self):
        
        # Arrange
        self._set_now(2025, 9, 12, 10, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Sep-12th-06:00h")
            
    def test_allows_same_day_but_later_time(self):
        
        # Arrange
        self._set_now(2025, 9, 12, 4, 0)

        # Act
        result = vh.try_parse_date_time("Sep-12th-06:00h")

        # Assert
        self.assertEqual(result, datetime(2025, 9, 12, 6, 0))

    def test_allows_january_date_when_now_is_december(self):
        
        # Arrange
        self._set_now(2025, 12, 20, 0, 0)

        # Act
        result = vh.try_parse_date_time("Jan-3rd-08:00h")

        # Assert
        self.assertEqual(result, datetime(2026, 1, 3, 8, 0))
    
    def test_rollover_only_applies_to_december_to_january(self):
        # Now is November; a January date should NOT get the rollover
        # exception, and should be treated as this-year (past) -> error.
        
        # Arrange
        self._set_now(2025, 11, 20, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Jan-3rd-08:00h")
            
    def test_rollover_does_not_apply_to_other_past_months_in_december(self):
        # Now is December; an October date is still in the past and
        # should NOT be excused by the rollover rule.
        
        # Arrange
        self._set_now(2025, 12, 20, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Oct-3rd-08:00h")
            
    def test_allows_feb_29_in_leap_year(self):
        
        # Arrange
        self._set_now(2024, 1, 1, 0, 0)  # 2024 is a leap year

        # Act
        result = vh.try_parse_date_time("Feb-29th-12:00h")

        # Assert
        self.assertEqual(result, datetime(2024, 2, 29, 12, 0))

    def test_raises_for_feb_29_in_non_leap_year(self):

        # Arrange
        self._set_now(2025, 1, 1, 0, 0)  # 2025 is not a leap year

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Feb-29th-12:00h")

    def test_feb_29_rollover_uses_next_year_for_leap_check(self):
        # Now is December 2023 (not leap). Feb isn't Jan, so the
        # rollover exception doesn't apply here; this is just a plain
        # in-year Feb 29 check against 2023 (not leap) -> should raise.
        
        # Arrange
        self._set_now(2023, 12, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Feb-29th-12:00h")
   
    def test_raises_on_empty_string(self):
        
        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("")

    def test_raises_on_whitespace_only_string(self):
        
        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("   ")

    def test_raises_on_none(self):
        
        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time(None)
            
    def test_raises_on_malformed_string(self):
        
        # Arrange        
        self._set_now(2025, 1, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("not a date")

    def test_raises_on_missing_time_component(self):

        # Arrange        
        self._set_now(2025, 1, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Sep-12th")

    def test_raises_on_invalid_month_name(self):

        # Arrange        
        self._set_now(2025, 1, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Septemb-12th-06:00h")

    def test_raises_on_missing_h_suffix_on_time(self):
        
        # Arrange        
        self._set_now(2025, 1, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Sep-12th-06:00")

    def test_raises_on_space_separators_instead_of_dashes(self):
        
        # Arrange        
        self._set_now(2025, 1, 1, 0, 0)

        # Act, Assert
        with self.assertRaises(ValueError):
            vh.try_parse_date_time("Sep 12th 06:00h")