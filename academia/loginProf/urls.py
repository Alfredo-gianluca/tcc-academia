from django.urls import path
from . import views

urlpatterns = [
    path('loginprof/', views.loginprof, name='loginprof'),
    path('logout/', views.logoutprof, name='logoutprof'),
]
