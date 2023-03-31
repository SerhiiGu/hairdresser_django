from django.shortcuts import render

from shop1.models import Service, Master, Calendar, Booking


def panel(request):
    return render(request, "panel.html")


def panel_services(request):
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
    if request.method == 'POST':
        master = Master(
            name=request.POST['name'],
            phone=request.POST['phone'],
            status=request.POST['status'],
            rang=request.POST['rang']
        )
        master.save()
        services_ids = [value for key, value in request.POST.items() if key.startswith('service')]
        for services_id in services_ids:
            service = Service.objects.get(id=services_id)
            master.services.add(service)
        master.save()
    masters = Master.objects.all()
    services = Service.objects.all()
    return render(request, 'panel_specialists.html', {'masters': masters, 'services': services})


def panel_one_specialist(request, specialist_id):
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
    bookings = Booking.objects.all()
    return render(request, 'panel_booking.html', {'bookings': bookings})


def panel_login(request):
    pass
