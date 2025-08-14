from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def cadastro(request):
    return render(request, 'cadastro.html', {
        'centralizar_logo': True
    })

# Create your views here.