from django.shortcuts import render
from django.http import HttpResponse
from loginProf.models import Professor
from django.shortcuts import redirect

def loginprof(request):
    erro = None  # variável para guardar a mensagem de erro

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            professor = Professor.objects.get(email=email, senha=senha)
            return redirect('TelaProf:lista_alunos')  # Redireciona para a lista de alunos após o login
        except Professor.DoesNotExist:
            erro = "Email ou senha inválidos."
            return render(request, 'loginprof.html', {
                'centralizar_logo': True,
                'erro': erro
            })

    return render(request, 'loginprof.html', {
        'centralizar_logo': True,
        'erro': erro
    })

# Create your views here.
