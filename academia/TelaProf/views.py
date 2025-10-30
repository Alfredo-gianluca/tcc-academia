from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import datetime

@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    return render(request, 'lista_alunos.html', {'alunos': alunos})


@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id)
    calendario = CalendarioFrequencia.objects.filter(usuario=aluno).order_by('-data')

    # --- Adicionar data de presença ---
    if request.method == 'POST':
        if 'adicionar_data' in request.POST:
            data_str = request.POST.get('nova_data')
            if data_str:
                try:
                    data = datetime.strptime(data_str, '%Y-%m-%d').date()
                    CalendarioFrequencia.objects.get_or_create(usuario=aluno, data=data)
                except ValueError:
                    pass  # data inválida, ignorar ou tratar com mensagem
            
        # --- Remover data de presença ---
        elif 'remover_data' in request.POST:
            data_id = request.POST.get('data_id')
            if data_id:
                CalendarioFrequencia.objects.filter(id=data_id, usuario=aluno).delete()

        # --- Atualizar observações ---
        elif 'salvar_observacoes' in request.POST:
            aluno.observacoes = request.POST.get('observacoes')
            aluno.save()

        return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

    return render(request, 'editar_aluno.html', {
        'aluno': aluno,
        'calendario': calendario,
    })

