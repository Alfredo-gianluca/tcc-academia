from django.urls import path
from . import views

urlpatterns = [
    path('', views.membros, name='membros'),
]