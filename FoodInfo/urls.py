from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'FoodInfo'

urlpatterns = [
    path('service/', views.service, name='service'),
    path('search/', views.search, name='search'),
    path('<int:food_id>/delete/', views.delete, name='delete'),
    path('<int:food_id>/update/', views.update, name='update'),
    path('getDate/', views.getDate, name='getDate'),
    path('getDateSearch/', views.getDateSearch, name='getDateSearch'),
    path('<int:food_id>/getDate/delete/', views.deleteByDate, name='deleteByDate'),
    path('<int:food_id>/getDate/update/', views.updateByDate, name='updateByDate')
]