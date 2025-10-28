from django.shortcuts import redirect, render
from cadastro.models import Usuario
from django.http import HttpResponse
from TelaAluno.views import TelaAluno

def login(request):
    erro = None  # variável para guardar a mensagem de erro

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            # salva o nome do usuário na sessão
            request.session['nome_usuario_completo'] = usuario.nome_completo
            # redireciona para a tela inicial
            return redirect('TelaAluno')

        except Usuario.DoesNotExist:
            erro = "Email ou senha inválidos."

    return render(request, 'login.html', {
        'centralizar_logo': True,
        'erro': erro
    })