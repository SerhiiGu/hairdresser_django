from django.test import TestCase
from django.test import Client
from shop1.models import Service, Master, Calendar
from django.contrib.auth.models import User


class TestAdminPanel(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin1', password='QWE123admin1ASD')
        user.save()

    def test_panel_services(self):
        c = Client()
        c.login(username='admin1', password='QWE123admin1ASD')
        response = c.post("/panel/services/", {"name": "Стрижка жіноча", "time": 45, "price": 500})
        self.assertEqual(response.status_code, 200)
        service = Service.objects.filter(name="Стрижка жіноча")
        self.assertEqual(len(service), 1)

    def test_panel_specialists(self):
        srv1 = Service(name="Стрижка бороди", time=15, price=100)
        srv1.save()
        srv2 = Service(name="Стрижка чоловіча", time=30, price=300)
        srv2.save()

        c = Client()
        c.login(username='admin1', password='QWE123admin1ASD')
        response = c.post("/panel/specialists/", {"name": "Регіна",
                                                  "status": 1,
                                                  "phone": 380671234567,
                                                  "rang": 1,
                                                  "service_1": srv1.id,
                                                  "service_2": srv2.id})
        self.assertEqual(response.status_code, 200)

        master = Master.objects.filter(name="Регіна")
        self.assertEqual(len(master), 1)

    def test_calendar_in_panel_one_specialist(self):
        srv1 = Service(name="Стрижка нова чоловіча", time=15, price=100)
        srv1.save()
        master = Master(name="Оксана", phone=234324, rang=1, status=1)
        master.save()
        master.services.add(srv1)
        master.save()

        c = Client()
        c.login(username='admin1', password='QWE123admin1ASD')
        response = c.post(f'/panel/specialist/{master.id}/', {
            "master": f'{master.id}',
            "date": "2023-04-07",
            "time_start": "10:00",
            "time_end": "11:00"
        }
                          )
        self.assertEqual(response.status_code, 200)

        calendar = Calendar.objects.filter(master=f'{master.id}')
        self.assertEqual(len(calendar), 1)
        self.assertEqual(master.name, "Оксана")
