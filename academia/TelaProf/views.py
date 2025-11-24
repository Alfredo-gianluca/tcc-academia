import json
from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    requisicoes = RequisicaoExclusao.objects.filter(status='pendente').select_related('usuario')
    
    # Pega a aba ativa (alunos ou requisicoes)
    aba_ativa = request.GET.get('aba', 'alunos')
    
    # Processa aprovação ou rejeição de requisição
    if request.method == 'POST':
        if 'aprovar_requisicao' in request.POST:
            requisicao_id = request.POST.get('requisicao_id')
            requisicao = get_object_or_404(RequisicaoExclusao, id=requisicao_id)
            
            # Deleta o usuário e marca a requisição como aprovada
            usuario = requisicao.usuario
            nome_usuario = usuario.nome_completo
            requisicao.status = 'aprovada'
            requisicao.save()
            usuario.delete()
            
            messages.success(request, f"Conta de {nome_usuario} excluída com sucesso.")
            return redirect('TelaProf:lista_alunos')
        
        elif 'rejeitar_requisicao' in request.POST:
            requisicao_id = request.POST.get('requisicao_id')
            requisicao = get_object_or_404(RequisicaoExclusao, id=requisicao_id)
            
            requisicao.status = 'rejeitada'
            requisicao.save()
            
            messages.info(request, f"Requisição de {requisicao.usuario.nome_completo} foi rejeitada.")
            return redirect('TelaProf:lista_alunos')
    
    return render(request, 'lista_alunos.html', {
        'alunos': alunos,
        'requisicoes': requisicoes,
        'aba_ativa': aba_ativa,
    })


@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id)
    calendario = CalendarioFrequencia.objects.filter(usuario=aluno).order_by('-data')
    cargas, _ = Cargas.objects.get_or_create(usuario=aluno)
    mes = int(request.GET.get('mes', datetime.now().month))
    ano = int(request.GET.get('ano', datetime.now().year))

    if request.method == 'POST':

        if 'adicionar_data' in request.POST:
            data_str = request.POST.get('nova_data')
            if data_str:
                try:
                    data = datetime.strptime(data_str, '%Y-%m-%d').date()
                    CalendarioFrequencia.objects.get_or_create(usuario=aluno, data=data)
                except ValueError:
                    pass

        elif 'remover_data' in request.POST:
            data_id = request.POST.get('data_id')
            if data_id:
                CalendarioFrequencia.objects.filter(id=data_id, usuario=aluno).delete()

        else:
            cargas.pernas = request.POST.get('pernas', '') or 0
            cargas.bracos = request.POST.get('bracos', '') or 0
            cargas.peito = request.POST.get('peito', '') or 0
            cargas.costas = request.POST.get('costas', '') or 0
            cargas.save()
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
                pass

        return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

    return render(request, 'editar_aluno.html', {
        'aluno': aluno,
        'calendario': calendario,
        'cargas': cargas,
        'mes': mes,
        'ano': ano,
    })