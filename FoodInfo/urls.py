from django.urls import path
from . import views

app_name = 'FoodInfo'

urlpatterns = [
    path('service/', views.service, name='service'),
    path('search/', views.search, name='search'),
    path('<int:food_id>/delete/', views.delete, name='delete'),
    path('<int:food_id>/update/', views.update, name='update'),
    path('getDate', views.getDate, name='getDate'),
]