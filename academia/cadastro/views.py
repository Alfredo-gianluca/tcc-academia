from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UsuarioCForm

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCForm(request.POST)
        if form.is_valid():
            usuario.senha = make_password(form.cleaned_data['senha'])
            usuario.save()
            form.save()
            return render(request, 'cadastroSucesso.html')
    else:
        form = UsuarioCForm()
    return render(request, 'cadastro.html', {
        'form': form,
        'centralizar_logo': True
    })

# Create your views here.