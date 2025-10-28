from django.shortcuts import render

def TelaAluno(request):
    nome = request.session.get('nome_usuario_completo', 'Usuário')
    return render(request, 'telainicial.html', {
        'centralizar_logo': False,
        'nome_usuario': nome
    })
