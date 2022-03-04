from django.urls import path
from cycle_angelo import views

app_name = 'cycle_angelo'

urlpatterns = [
path('', views.index, name='index'),
path('add_post/', views.add_post, name='add_post'),
path('post/<slug:post_name_slug>/',
         views.show_post, name='show_post'),
path('post/<slug:post_name_slug>/add_comment/',
         views.add_comment, name='add_comment'),


]
