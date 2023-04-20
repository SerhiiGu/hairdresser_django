import datetime
import warnings

from django.test import TestCase
from shop1.utils.periods_calc_tests import convert_period_to_set, calc_free_time_in_day

from django.test import Client
from django.contrib.auth.models import User
from shop1.models import Service, Master, Booking, Calendar


warnings.filterwarnings("ignore", category=RuntimeWarning)


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


class TestBooking(TestCase):
    fixtures = ['fixture1.json']

    def test_booking(self):
        service1 = Service.objects.filter(name__contains="Стрижка жіноча").first()
        master1 = Master(name="Регіна", phone=38012234324, rang=1, status=1)
        master1.save()
        master1.services.add(service1)
        master1.save()
        calendar1 = Calendar(master=master1, date="2023-04-25 00:00:00", time_start="11:00", time_end="13:00")
        calendar1.save()
    # Просте резервування
        c = Client()
        c.login(username='user1', password='123qwe123')
        response = c.post(f'/booking/{master1.id}/{service1.id}/', {"date": "2023-04-25 11:30"})
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.filter(master=master1, service=service1, date="2023-04-25 11:30")
        self.assertEqual(len(booking), 1)
    # Два резервування на різні проміжки
        response = c.post(f'/booking/{master1.id}/{service1.id}/', {"date": "2023-04-25 11:00"})
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.filter(master=master1, service=service1, date="2023-04-25 11:00")
        self.assertEqual(len(booking), 1)

        response = c.post(f'/booking/{master1.id}/{service1.id}/', {"date": "2023-04-25 12:15"})
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.filter(master=master1, service=service1)
        self.assertEqual(len(booking), 3)
        # --------------------------------------------
        service2 = Service(name="Стрижка супернова жіноча", time=45, price=500)
        service2.save()
        service3 = Service(name="Стрижка супернова чоловіча", time=30, price=250)
        service3.save()
        master2 = Master(name="Світлана Сайкович", phone=380661234567, rang=2, status=1)
        master2.save()
        master2.services.add(service2)
        master2.save()
        master2.services.add(service3)
        master2.save()
        calendar2 = Calendar(master=master2, date="2023-04-25 00:00:00", time_start="11:00", time_end="13:00")
        calendar2.save()
    # Тест на резерв, коли двоє завантажили сторінку одночасно і вибрали один час з одного слоту,
    # проте один довго думав(сторінка була відкрита і не перезавантажувалася), і за цей час частину слоту зайняли
        c = Client()
        c.login(username='user1', password='123qwe123')
        response = c.post(f'/booking/{master2.id}/{service2.id}/', {"date": "2023-04-25 11:30"})
        self.assertEqual(response.status_code, 200)
        booking = Booking.objects.filter(master=master2, service=service2, date="2023-04-25 11:30")
        self.assertEqual(len(booking), 1)

        response = c.post(f'/booking/{master2.id}/{service3.id}/', {"date": "2023-04-25 11:45"})
        self.assertContains(response, "На жаль, даний проміжок часу чи його частина уже зайнята")
