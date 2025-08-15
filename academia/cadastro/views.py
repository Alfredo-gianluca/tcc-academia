from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponseForbidden


def cadastro(request):
    referer = request.META.get('HTTP_REFERER')

    # Permitir apenas se veio da tela inicial (ajuste conforme necessário)
    if referer is None or not referer.startswith('http://127.0.0.1:8000/'):
        return HttpResponseForbidden("Acesso direto não permitido.")

    return render(request, 'cadastro.html', {
        'centralizar_logo': True
    })

# Create your views here.