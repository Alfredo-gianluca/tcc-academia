from django.shortcuts import render
from django.http import HttpResponse
from loginProf.models import Professor

def loginprof(request):
    erro = None  # variável para guardar a mensagem de erro

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            professor = Professor.objects.get(email=email, senha=senha)
            return HttpResponse(f"Bem-vindo, {professor.nome_completo}!")
        except Professor.DoesNotExist:
            erro = "Email ou senha inválidos."

    return render(request, 'loginprof.html', {
        'centralizar_logo': True,
        'erro': erro
    })

# Create your views here.
