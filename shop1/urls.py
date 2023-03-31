from django.urls import path
import shop1.views


urlpatterns = [
    path('', shop1.views.root_handler, name='root_handler'),
    path('services/', shop1.views.services_handler, name='services'),
    path('services/<int:service_id>/', shop1.views.service_id_handler),
    path('specialist/', shop1.views.specialist_handler, name='specialist'),
    path('specialist/<int:specialist_id>/', shop1.views.specialist_id_handler),
    path('booking/', shop1.views.booking_handler, name='booking'),
    path('user/', shop1.views.user_page),
    path('login/', shop1.views.login_handler, name='login'),
    path('register/', shop1.views.register_handler, name='register'),
]
