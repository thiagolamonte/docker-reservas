from django.urls import path

from core import views

app_name = 'core'


urlpatterns = [
    path('', views.index, name='index'),
    path('quarto/list/', views.quarto_list, name='quarto-list'),
    path('quarto/add/', views.quarto_add, name='quarto-add'),
    path('quarto/<int:quarto_id>/change/', views.quarto_change, name='quarto-change'),
    path('reserva/list/', views.reserva_list, name='reserva-list'),
    path('reserva/add/', views.reserva_add, name='reserva-add'),
    path('reserva/<int:reserva_id>/change/', views.reserva_change, name='reserva-change'),
    path('reserva/calendar/', views.reserva_calendar, name='reserva-calendar'),
]
