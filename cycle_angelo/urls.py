from django.urls import path
from cycle_angelo import views

app_name = 'cycle_angelo'

urlpatterns = [
path('', views.index, name='index'),
]
