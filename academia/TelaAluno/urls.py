from django.urls import path
from . import views

app_name = 'TelaAluno'

urlpatterns = [
    path('Interface_de_usuário/', views.TelaAluno, name='telaaluno'),
    path('nutricao/', views.nutricao, name='nutricao'),
]
