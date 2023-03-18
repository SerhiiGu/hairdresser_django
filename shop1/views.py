from django.http import HttpResponse
from django.shortcuts import render


def root_handler(request):
    return render(request, "index.html")


def services_handler(request):
    return HttpResponse("Service page!")


def service_id_handler(request, service_id):
    return HttpResponse("Service page of %s!" % service_id)


def specialist_handler(request):
    return HttpResponse("Specialist page")


def specialist_id_handler(request, specialist_id):
    return HttpResponse("Specialist %s page" % specialist_id)


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
    return HttpResponse("login_handler")


def register_handler(request):
    return HttpResponse("register_handler")
