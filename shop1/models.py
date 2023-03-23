from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    time = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Master(models.Model):
    RANG_CHOICES = (
        (0, 'Rang 1'),
        (1, 'Rang 2')
    )
    name = models.CharField(max_length=100)
    rang = models.IntegerField(default=0, choices=RANG_CHOICES)
    phone = models.IntegerField()
    status = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name


class Booking(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.master} {self.service} {self.client} {self.date}'


class Calendar(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return f'{self.master} {self.date}'
