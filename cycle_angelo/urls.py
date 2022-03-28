from django.urls import path, include
from cycle_angelo import views
from cycle_angelo.models import User

app_name = 'cycle_angelo'

urlpatterns = [
path('', views.index, name='index'),
path('add_post/', views.add_post, name='add_post'),
path('post/<slug:post_name_slug>/',
         views.show_post, name='show_post'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('register_profile/', views.register_profile, name='register_profile'),
path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
path('contact_us/', views.contact_us, name="contact_us"),
path('like_post/', views.LikePostView.as_view(), name='like_post'),


]
