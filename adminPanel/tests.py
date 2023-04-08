from django.test import TestCase
from django.test import Client
from shop1.models import Service, Master, Calendar


class Test(TestCase):
    def test_panel_services(self):
        c = Client()
        response = c.post("/panel/services/", {"name": "Some service 1", "time": 45, "price": 500})
        self.assertEqual(response.status_code, 200)
        service = Service.objects.filter(name="Some service 1")
        self.assertEqual(len(service), 1)

    def test_panel_specialists(self):
        srv1 = Service(name="name 1", time=15, price=100)
        srv1.save()
        srv2 = Service(name="name 2", time=30, price=300)
        srv2.save()
        # !!!!!!
        c = Client()
        response = c.post("/panel/specialists/", {"name": "Регіна", "status": 1,
                                                  "phone": 380671234567, "rang": 1, "service_1": 1, "service_2": 2})
        self.assertEqual(response.status_code, 200)

        master = Master.objects.filter(name="Регіна")
        self.assertEqual(len(master), 1)

    def test_calendar_in_panel_one_specialist(self):
        srv1 = Service(name="name 1", time=15, price=100)
        srv1.save()
        master = Master(name="Регіна", phone=234324, rang=1, status=1)
        master.save()
        master.services.add(srv1)
        master.save()

        c = Client()
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
