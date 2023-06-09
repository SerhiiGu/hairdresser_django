from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from shop1.models import Service, Master, Calendar, Booking


def panel(request):
    if not request.user.has_perm('shop1.add_master'):
        return render(request, "panel.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    return render(request, "panel.html")


def panel_services(request):
    if not request.user.has_perm('shop1.add_service'):
        return render(request, "panel_services.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    if request.method == 'POST':
        service = Service(
            name=request.POST['name'],
            price=request.POST['price'],
            time=request.POST['time']
        )
        service.save()
    services = Service.objects.all()
    return render(request, 'panel_services.html', {'services': services})


def panel_specialists(request):
    if not request.user.has_perm('shop1.add_master'):
        return render(request, "panel_specialists.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    without_service_selected = 0
    if request.method == 'POST':
        services_ids = [value for key, value in request.POST.items() if key.startswith('service')]
        if len(services_ids) > 0:
            master = Master(
                name=request.POST['name'],
                phone=request.POST['phone'],
                status=request.POST['status'],
                rang=request.POST['rang']
            )
            master.save()
            for services_id in services_ids:
                service = Service.objects.get(id=services_id)
                master.services.add(service)
            master.save()
        else:
            without_service_selected = 1
    masters = Master.objects.all()
    services = Service.objects.all()
    return render(request, 'panel_specialists.html', {'masters': masters,
                                                      'services': services,
                                                      'without_service_selected': without_service_selected})


def panel_one_specialist(request, specialist_id):
    if not request.user.has_perm('shop1.add_master'):
        return render(request, "panel_one_specialist.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    if request.method == 'POST':
        shedule = Calendar(
            master=Master.objects.get(id=specialist_id),
            date=request.POST['date'],
            time_start=request.POST['time_start'],
            time_end=request.POST['time_end']
        )
        shedule.save()
    current_master = Master.objects.get(id=specialist_id)
    shedule = Calendar.objects.filter(master=current_master).all()
    return render(request, 'panel_one_specialist.html', {'shedule': shedule})


def panel_booking(request):
    if not request.user.has_perm('shop1.add_master'):
        return render(request, "panel_booking.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    bookings = Booking.objects.all()
    page_num = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 999)
    error = ''
    if (int(page_num) - 1) * int(per_page) > bookings.count():
        error = f'Запит викодить за межі кількості записів в базі: {bookings.count()}'
    pages = Paginator(bookings, per_page)
    return render(request, 'panel_booking.html', {'bookings': pages.get_page(page_num).object_list, 'error': error})


def panel_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/panel/')
        else:
            return render(request, "panel_login.html", {"error": "Помилка в логіні/паролі, або ж неіснуючий користувач!"})
    return render(request, "panel_login.html")


def panel_logout(request):
    logout(request)
    return redirect('panel_login')
