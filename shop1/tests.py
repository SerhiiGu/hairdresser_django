import datetime

from django.test import TestCase
from shop1.utils.periods_calc_tests import convert_period_to_set, calc_free_time_in_day


class PeriodsCalcTests(TestCase):
    def test_convert_period_to_set(self):
        time_start = datetime.datetime(2023, 5, 5, 9, 0)
        time_end = datetime.datetime(2023, 5, 5, 10, 0)

        result = convert_period_to_set(time_start, time_end)
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 0),
            datetime.datetime(2023, 5, 5, 9, 15),
            datetime.datetime(2023, 5, 5, 9, 30),
            datetime.datetime(2023, 5, 5, 9, 45),
            datetime.datetime(2023, 5, 5, 10, 0)
        }
        self.assertSetEqual(result, expected_result)

    def test_string_convert_period_to_set(self):
        time_start = 'start'
        time_end = datetime.datetime(2023, 5, 5, 10, 0)
        with self.assertRaises(TypeError):
            convert_period_to_set(time_start, time_end)

    def test_reverse_convert_period_to_set(self):
        time_start = datetime.datetime(2023, 5, 5, 10, 0)
        time_end = datetime.datetime(2023, 5, 5, 9, 0)

        result = convert_period_to_set(time_start, time_end)
        expected_result = set()
        self.assertSetEqual(result, expected_result)

    def test_equal_convert_period_to_set(self):
        time_start = datetime.datetime(2023, 5, 5, 9, 0)
        time_end = datetime.datetime(2023, 5, 5, 9, 0)

        result = convert_period_to_set(time_start, time_end)
        expected_result = {datetime.datetime(2023, 5, 5, 9, 0)}
        self.assertSetEqual(result, expected_result)

    def test_calc_free_time_in_day_with_one_booking(self):
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 30
            }
        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 0),
            datetime.datetime(2023, 5, 5, 9, 15),
            datetime.datetime(2023, 5, 5, 9, 30),
            datetime.datetime(2023, 5, 5, 10, 30)
        }
        self.assertSetEqual(result, expected_result)

    def test_calc_free_time_in_day_with_timedelta_two_bookings(self):
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 15),
                'service_time': 15
            }
        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 30),
            datetime.datetime(2023, 5, 5, 10, 30)
        }
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 15),
                'service_time': 45
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 30),
                'service_time': 15
            }
        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 10, 0)
        }
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 45
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 15),
                'service_time': 30
            }
        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = set()
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 30),
                'service_time': 45
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 45),
                'service_time': 15
            }
        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 0),
            datetime.datetime(2023, 5, 5, 10, 15)
        }
        self.assertSetEqual(result, expected_result)

    def test_calc_free_time_in_day_with_timedelta_three_bookings(self):
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 15),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 45),
                'service_time': 15
            }

        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = set()
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 30),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 15
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 15),
                'service_time': 15
            }

        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 0),
            datetime.datetime(2023, 5, 5, 10, 30)
        }
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 30),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 15
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 45),
                'service_time': 15
            }

        ]
        service_time = 15
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 9, 0),
            datetime.datetime(2023, 5, 5, 9, 15),
            datetime.datetime(2023, 5, 5, 10, 15),
            datetime.datetime(2023, 5, 5, 10, 30)
        }
        self.assertSetEqual(result, expected_result)
        # --------------------------------------------
        bookings = [
            {
                'date_time': datetime.datetime(2023, 5, 5, 9, 15),
                'service_time': 30
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 0),
                'service_time': 15
            },
            {
                'date_time': datetime.datetime(2023, 5, 5, 10, 15),
                'service_time': 15
            }

        ]
        service_time = 30
        workdate_date = datetime.datetime(2023, 5, 5, 0, 0)
        workday_time_start = datetime.time(9, 0)
        workday_time_end = datetime.time(11, 0)
        result = set(calc_free_time_in_day(bookings, service_time,
                                           workdate_date, workday_time_start, workday_time_end))
        expected_result = {
            datetime.datetime(2023, 5, 5, 10, 30)
        }
        self.assertSetEqual(result, expected_result)
