import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import utc

from shop1.models import Service, Master, Calendar, Booking
from shop1.utils.periods_calc import get_free_slots_for_booking


def root_handler(request):
    return render(request, "index.html")


@login_required(login_url='/login/')
def services_handler(request):
    calendars = Calendar.objects.filter(date__gte=datetime.datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=utc),
        date__lte=datetime.datetime.today().replace(tzinfo=utc) + datetime.timedelta(days=7)).all()
    master_ids = []
    for name in calendars:
        master_ids.append(Calendar.objects.filter(master=name.master).first().master_id)
    available_masters = [name.id for name in Master.objects.filter(id__in=master_ids, status=True).all()]
    available_services = [service.id for service in Service.objects.filter(master__id__in=available_masters).distinct().all()]
    services = [name.name for name in Service.objects.filter(id__in=available_services).all()]
    services_dict = {service.id: service.name for service in Service.objects.filter(name__in=services).all()}
    return render(request, "services.html", {'services_dict': services_dict})


@login_required(login_url='/login/')
def service_id_handler(request, service_id):
    service_name = Service.objects.filter(id=service_id).first().name
    calendars = Calendar.objects.filter(date__gte=datetime.datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=utc),
        date__lte=datetime.datetime.today().replace(tzinfo=utc) + datetime.timedelta(days=7)).all()
    master_ids = []
    for name in calendars:
        master_ids.append(Calendar.objects.filter(master=name.master).first().master_id)
    available_masters = {row.id: row.name for row in Master.objects.filter(id__in=master_ids, status=True).all()}
    return render(request, "service.html", {'service_id': service_id,
                                            'service_name': service_name,
                                            'masters': available_masters})


@login_required(login_url='/login/')
def specialist_handler(request):
    calendars = Calendar.objects.filter(date__gte=datetime.datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=utc),
        date__lte=datetime.datetime.today().replace(tzinfo=utc) + datetime.timedelta(days=7)).all()
    master_ids = []
    for name in calendars:
        master_ids.append(Calendar.objects.filter(master=name.master).first().master_id)
    available_masters = {row.id: row.name for row in Master.objects.filter(id__in=master_ids, status=True).all()}
    return render(request, "specialist.html", {'masters': available_masters})


@login_required(login_url='/login/')
def specialist_id_handler(request, specialist_id):
    name = Master.objects.filter(id=specialist_id, status=True).first().name
    services_ids = {row.id: row.name for row in Service.objects.filter(master=specialist_id).all()}
    return render(request, "specialist_id.html", {'specialist_id': specialist_id, 'name': name, 'services': services_ids})


@login_required(login_url='/login/')
def service_booking_handler(request, specialist_id, service_id):
    if request.user.has_perm('shop1.add_master'):
        return render(request, "index.html",
                      {"error": "Адміни не можуть бронювати замовлення! Увійдіть як користувач"})
    master_name = Master.objects.filter(id=specialist_id, status=True).first().name
    service_name = Service.objects.filter(id=service_id).first().name
    if request.method == 'POST':
        set_datetime_object = set()
        datetime_object = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d %H:%M")
        set_datetime_object.add(datetime_object)
        free_work_slots = set(get_free_slots_for_booking(specialist_id, service_id))
        if len(free_work_slots.intersection(set_datetime_object)) > 0:
            booking = Booking(
                master=Master.objects.get(id=specialist_id),
                service=Service.objects.get(id=service_id),
                client=request.user.pk,
                date=datetime_object
            )
            booking.save()
            return render(request, "booking_complete.html")
        else:
            return render(request, 'booking.html', {
                'master_name': master_name,
                'service_name': service_name,
                'free_work_slots': free_work_slots,
                'got_error': "slot is busy now"})

    free_work_slots = get_free_slots_for_booking(specialist_id, service_id)
    return render(request, 'booking.html', {
        'master_name': master_name,
        'service_name': service_name,
        'free_work_slots': free_work_slots})


def user_page(request):
    return HttpResponse("User page")


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {"error": "Помилка в логіні/паролі, або ж неіснуючий користувач!"})
    return render(request, "login.html")


def logout_handler(request):
    logout(request)
    return redirect('login')


def register_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('/login/')
        else:
            return render(request, "register.html", {"error": "Щось пішло не так, спробуйте знову"})
    return render(request, "register.html")
