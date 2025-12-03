from django.shortcuts import redirect, render
from cadastro.models import Usuario

def login(request):
    errors = []
    email_value = ""

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        email_value = email

        try:
            usuario = Usuario.objects.get(email=email)

            if senha == usuario.senha:
                # Criar sessão da forma correta
                request.session['aluno_autenticado'] = True
                request.session['aluno_id'] = usuario.id
                request.session['aluno_nome'] = usuario.nome_completo

                return redirect('TelaAluno:telaaluno')
            else:
                errors.append("Email ou senha incorretos.")

        except Usuario.DoesNotExist:
            errors.append("Email ou senha incorretos.")

    return render(request, 'login.html', {
        "errors": errors,
        "email": email_value
    })

def logout_aluno(request):
    # Apaga todos os dados da sessão do aluno
    request.session.flush()  # limpa toda a sessão
    
    # Redireciona para a página de login
    return redirect('login')