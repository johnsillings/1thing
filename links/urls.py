from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('submit/', views.submit_link, name='submit_link'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
