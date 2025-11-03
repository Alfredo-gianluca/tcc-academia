from django.shortcuts import redirect, render
from cadastro.models import Usuario
from django.http import HttpResponse
from TelaAluno.views import TelaAluno
from django.contrib import messages
from TelaAluno.urls import urlpatterns as telaaluno_urls

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            usuario = Usuario.objects.get(email=email)
            
            # Verifica a senha (adapte conforme sua implementação)
            if senha == usuario.senha:  # ou sua verificação
                # SALVAR NA SESSÃO
                request.session['usuario_id'] = usuario.id  # ← IMPORTANTE
                request.session['nome_usuario_completo'] = usuario.nome_completo
                
                return redirect('telaaluno')
            else:
                messages.error(request, 'Senha incorreta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
    
    return render(request, 'login.html')