from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    return render(request, 'lista_alunos.html', {'alunos': alunos})


@login_required
def editar_aluno(request, aluno_id, CalendarioFrequencia_id=None):
    aluno = get_object_or_404(Usuario, id=aluno_id)
    calendario = CalendarioFrequencia.objects.filter(usuario=aluno)

    if request.method == 'POST':
        aluno.observacoes = request.POST.get('observacoes')
        calendario = CalendarioFrequencia.objects.filter(usuario=aluno)

        for data in calendario:
            data.presente = request.POST.get(f'presente_{data.id}') == 'on'
            data.save()

        aluno.save()
        return redirect('TelaProf:lista_alunos')

    return render(request, 'editar_aluno.html', {'aluno': aluno, 'calendario': calendario})

# Create your views here.
