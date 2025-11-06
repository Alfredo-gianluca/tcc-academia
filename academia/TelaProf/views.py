import json
from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    return render(request, 'lista_alunos.html', {'alunos': alunos})


@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id)
    calendario = CalendarioFrequencia.objects.filter(usuario=aluno).order_by('-data')

    if request.method == 'POST':

        # --- Adicionar nova data ---
        if 'adicionar_data' in request.POST:
            data_str = request.POST.get('nova_data')
            if data_str:
                try:
                    data = datetime.strptime(data_str, '%Y-%m-%d').date()
                    CalendarioFrequencia.objects.get_or_create(usuario=aluno, data=data)
                except ValueError:
                    pass  # Data inválida

        # --- Remover data ---
        elif 'remover_data' in request.POST:
            data_id = request.POST.get('data_id')
            if data_id:
                CalendarioFrequencia.objects.filter(id=data_id, usuario=aluno).delete()

        # --- Salvar observações e presenças ---
        else:
            aluno.observacoes = request.POST.get('observacoes', '')
            aluno.save()

            presencas_json = request.POST.get('presencas_json', '{}')
            try:
                presencas_data = json.loads(presencas_json)
                for freq_id, presente in presencas_data.items():
                    try:
                        freq = CalendarioFrequencia.objects.get(id=freq_id, usuario=aluno)
                        freq.presente = bool(presente)
                        freq.save()
                    except CalendarioFrequencia.DoesNotExist:
                        pass
            except json.JSONDecodeError:
                pass  # Ignora se o JSON vier malformado

        return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

    return render(request, 'editar_aluno.html', {
        'aluno': aluno,
        'calendario': calendario,
    })