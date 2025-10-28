from django.urls import path
from . import views

urlpatterns = [
    path('Interface_de_usuário/', views.TelaAluno, name='TelaAluno'),
]
