from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .forms import UsuarioForm
from datetime import date, timedelta
from .models import CalendarioFrequencia, Cargas

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = form.cleaned_data['senha']
            usuario.save()
            
            # Gera as datas automaticamente no calendário
            inicio = date(2025, 1, 1)   # ajuste o período
            fim = date(2025, 12, 31)
            delta = timedelta(days=1)
            data_atual = inicio

            # Gera as cargas iniciais automaticamente
            Cargas.objects.create(
                usuario=usuario,
                pernas=0,
                bracos=0,
                costas=0,
                peito=0
            )

            while data_atual <= fim:
                # opcional: pula finais de semana
                if data_atual.weekday() < 5:  # 0=segunda, 6=domingo
                    CalendarioFrequencia.objects.create(
                        usuario=usuario,
                        data=data_atual
                    )
                data_atual += delta

            return render(request, 'cadastroSucesso.html')
    else:
        form = UsuarioForm()

    return render(request, 'cadastro.html', {
        'form': form,
        'centralizar_logo': True
    })

# Create your views here.