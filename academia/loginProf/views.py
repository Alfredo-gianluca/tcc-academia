from django.shortcuts import redirect, render
from loginProf.models import Professor

def loginprof(request):
    errors = []  # variável para guardar a mensagem de erro
    email_value = ""

    if request.session.get('professor_autenticado'):
        return redirect('TelaProf:lista_alunos')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        email_value = email

        try:
            professor = Professor.objects.get(email=email)
            
            if senha == professor.senha:
                # Criar sessão da forma correta
                request.session['professor_autenticado'] = True
                request.session['professor_id'] = professor.id
                request.session['professor_nome'] = professor.nome_completo

                return redirect('TelaProf:lista_alunos')
            else:
                errors.append("Email ou senha incorretos.")

        except Professor.DoesNotExist:
            errors.append("Email ou senha incorretos.")

    return render(request, 'loginprof.html', {
        'centralizar_logo': True,
        'errors': errors, 
        'email': email_value
    })

def logoutprof(request):
    # Apaga todos os dados da sessão do professor
    request.session.flush()  # limpa toda a sessão
    
    # Redireciona para a página de login
    return redirect('loginprof')
# Create your views here.