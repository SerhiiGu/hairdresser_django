from django.urls import path
import shop1.views


urlpatterns = [
    path('', shop1.views.root_handler),
    path('services/', shop1.views.services_handler),
    path('services/<int:service_id>/', shop1.views.service_id_handler),
    path('specialist/', shop1.views.specialist_handler),
    path('specialist/<specialist_id>/', shop1.views.specialist_id_handler),
    path('booking/', shop1.views.booking_handler),
    path('user/', shop1.views.user_page),
    path('panel/', shop1.views.panel_page),
    path('panel/booking/', shop1.views.panel_booking_page),
    path('panel/specialist/', shop1.views.panel_specialist_page),
    path('panel/specialist/<specialist_id>', shop1.views.panel_specialist_id_page),
    path('login/', shop1.views.login_handler),
    path('register/', shop1.views.register_handler),
]
