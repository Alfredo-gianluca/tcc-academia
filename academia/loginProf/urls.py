from django.urls import path
from . import views

urlpatterns = [
    path('loginprof/', views.loginprof, name='loginprof'),
]
