from django.urls import path
from . import views

app_name = 'TelaProf'

urlpatterns = [
    path('lista_alunos/', views.lista_alunos, name='lista_alunos'),
    path('editar_aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    # Adicione outras URLs conforme necessário
    # path('outra_view/', views.outra_view, name='outra_view'),
]