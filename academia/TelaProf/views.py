from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    return render(request, 'lista_alunos.html', {'alunos': alunos})


@login_required
def editar_aluno(request, aluno_id):

    aluno = get_object_or_404(Usuario, id=aluno_id)

    if request.method == 'POST':
        aluno.observacoes = request.POST.get('observacoes')
        aluno.save()
        return redirect('TelaProf:lista_alunos')

    return render(request, 'editar_aluno.html', {'aluno': aluno})


# Create your views here.
