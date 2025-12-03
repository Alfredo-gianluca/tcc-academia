from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_aluno, name='logout_aluno'),
]