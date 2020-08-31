from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'FoodInfo'

urlpatterns = [
    path('service/', views.service, name='service'),
    path('search/', views.search, name='search'),
    path('<int:food_id>/delete/', views.delete, name='delete'),
    path('<int:food_id>/update/', views.update, name='update'),
    path('service/<int:inputDate>', views.getDate),
    path('<int:urlDate>/service/', views.serviceByDate, name='serviceByDate'),
    path('<int:urlDate>/search/', views.searchByDate, name='searchByDate'),
    #path('<int:inputDate>/service/', views.getDate, name= 'researchDate'),
    path('<int:urlDate>/delete/<int:food_id>', views.deleteByDate, name='deleteByDate'),
    path('<int:urlDate>/update/<int:food_id>', views.updateByDate, name='updateByDate'),
]