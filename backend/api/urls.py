from django.urls import path

from . import views

urlpatterns = [
    path('vehicles/', views.get_vehicles, name='vehicles'),
    path('vehicles/<int:vehicle_id>/', views.get_vehicle_detail, name='vehicle-detail'),
    path('summary/', views.get_summary, name='summary'),
]
