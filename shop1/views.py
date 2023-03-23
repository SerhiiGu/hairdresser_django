import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import utc

from shop1.models import Service, Master, Calendar


def root_handler(request):
    return render(request, "index.html")


def services_handler(request):
    calendars = Calendar.objects.filter(date__gte=datetime.datetime.today().replace(tzinfo=utc),
        date__lte=datetime.datetime.today().replace(tzinfo=utc) + datetime.timedelta(days=7)).all()
    master_ids = []
    for name in calendars:
        master_ids.append(Calendar.objects.filter(master=name.master).first().id)
    available_masters = [name.id for name in Master.objects.filter(id__in=master_ids, status=True).all()]
    available_services = [service.id for service in Service.objects.filter(master__id__in=available_masters).distinct().all()]
    services = [name.name for name in Service.objects.filter(id__in=available_services).all()]
    services_dict = {service.id: service.name for service in Service.objects.filter(name__in=services).all()}
    return render(request, "services.html", {'services_dict': services_dict})


def service_id_handler(request, service_id):
    service_name = Service.objects.filter(id=service_id).first().name
    # masters = [name.name for name in Master.objects.filter(services=service_id).all()]
    masters = {name.id: name.name for name in Master.objects.filter(services=service_id, status=True).all()}
    return render(request, "service.html", {'service_name': service_name, 'masters': masters})


def specialist_handler(request):
    calendars = Calendar.objects.filter(date__gte=datetime.datetime.today().replace(tzinfo=utc),
        date__lte=datetime.datetime.today().replace(tzinfo=utc) + datetime.timedelta(days=7)).all()
    master_ids = []
    for name in calendars:
        master_ids.append(Calendar.objects.filter(master=name.master).first().id)
    available_masters = {row.id: row.name for row in Master.objects.filter(id__in=master_ids, status=True).all()}
    return render(request, "specialist.html", {'masters': available_masters})


def specialist_id_handler(request, specialist_id):
    name = Master.objects.filter(id=specialist_id, status=True).first().name
    services_ids = {row.id: row.name for row in Service.objects.filter(master=specialist_id).all()}
    return render(request, "specialist_id.html", {'name': name, 'services': services_ids})


def booking_handler(request):
    return HttpResponse("Booking page")


def user_page(request):
    return HttpResponse("User page")


def panel_page(request):
    return HttpResponse("User panel page")


def panel_booking_page(request):
    return HttpResponse("panel_booking_page")


def panel_specialist_page(request):
    return HttpResponse("panel_specialist_page")


def panel_specialist_id_page(request):
    return HttpResponse("panel_specialist_id_page")


def login_handler(request):
    return render(request, "login.html")


def register_handler(request):
    return render(request, "register.html")
