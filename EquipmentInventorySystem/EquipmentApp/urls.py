from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('equipments/', views.equipment_list, name='equipment_list'),
    path('equipments/add/', views.equipment_create, name='equipment_create'),
    path('equipments/<int:equipment_id>/edit/', views.equipment_update, name='equipment_update'),
    path('equipments/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
]