from django.shortcuts import render
from cadastro.models import Usuario
from django.http import HttpResponse

def login(request):
    erro = None  # variável para guardar a mensagem de erro

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            return HttpResponse(f"Bem-vindo, {usuario.nome_completo}!")
        except Usuario.DoesNotExist:
            erro = "Email ou senha inválidos."

    return render(request, 'login.html', {
        'centralizar_logo': True,
        'erro': erro
    })