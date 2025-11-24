from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('membros.urls')),
    path('', include('cadastro.urls')),
    path('', include('login.urls')),
    path('', include('loginProf.urls')),
    path('', include('TelaProf.urls')),
    path('', include('TelaAluno.urls')),
    path('admin/', admin.site.urls)
]
