from django.urls import path
import adminPanel.views


urlpatterns = [
    path('', adminPanel.views.panel, name='panel_root'),
    path('services/', adminPanel.views.panel_services, name='panel_services'),
    path('specialists/', adminPanel.views.panel_specialists, name='panel_specialists'),
    path('specialist/<specialist_id>/', adminPanel.views.panel_one_specialist),
    path('booking/', adminPanel.views.panel_booking, name='panel_booking'),
    path('login/', adminPanel.views.panel_login, name='panel_login'),
    path('logout/', adminPanel.views.panel_logout, name='panel_logout'),
    ]
