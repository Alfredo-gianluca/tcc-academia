import json
from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao, HistoricoAtividades, Ficha
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime


@login_required
def lista_alunos(request):
    alunos = Usuario.objects.all()
    requisicoes = RequisicaoExclusao.objects.filter(status='pendente').select_related('usuario')
    
    aba_ativa = request.GET.get('aba', 'alunos')
    
    if request.method == 'POST':
        if 'aprovar_requisicao' in request.POST:
            requisicao_id = request.POST.get('requisicao_id')
            requisicao = get_object_or_404(RequisicaoExclusao, id=requisicao_id)
            
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
    historico = HistoricoAtividades.objects.filter(usuario=aluno).order_by('-data')
    cargas, _ = Cargas.objects.get_or_create(usuario=aluno)

    mes = int(request.GET.get('mes', datetime.now().month))
    ano = int(request.GET.get('ano', datetime.now().year))

    if request.method == 'POST':

        # BLOQUEIA criação de datas
        if "adicionar_data" in request.POST:
            messages.error(request, "Não é permitido adicionar novas datas.")
            return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

        # ADICIONAR HISTÓRICO
        elif 'adicionar_historico' in request.POST:
            data_str = request.POST.get('data_historico')
            treino = request.POST.get('treino_historico')
            qtd = request.POST.get('qtd_exercicios')
            cargas = request.POST.get('cargas_historico', 0)

            # Se clicou no botão mas deixou campos vazios
            if not data_str or not treino or not qtd:
                messages.error(request, "Preencha todos os campos do histórico antes de adicionar.")
                return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').date()

                # Só pode adicionar histórico se a data for PRESENTE
                freq = CalendarioFrequencia.objects.filter(
                    usuario=aluno, data=data, presente=True
                ).first()

                if not freq:
                    messages.error(
                        request, 
                        f"❌ A data {data.strftime('%d/%m/%Y')} NÃO está presente no calendário!"
                    )
                    return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

                # Impede histórico duplicado
                if HistoricoAtividades.objects.filter(usuario=aluno, data=data).exists():
                    messages.warning(
                        request, 
                        f"Já existe um histórico registrado em {data.strftime('%d/%m/%Y')}."
                    )
                else:
                    HistoricoAtividades.objects.create(
                        usuario=aluno,
                        data=data,
                        Treino=treino,
                        qtdexercicios=qtd,
                    )
                    messages.success(request, "Histórico adicionado com sucesso!")

            except ValueError:
                messages.error(request, "Data inválida.")
                
            return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

        # REMOVER HISTÓRICO
        elif 'remover_historico' in request.POST:
            historico_id = request.POST.get('historico_id')
            hist = HistoricoAtividades.objects.filter(
                id=historico_id, usuario=aluno
            ).first()

            if hist:
                hist.delete()
                messages.success(request, "Histórico removido!")
            
            return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

        # SALVAR CARGAS + PRESENÇAS
        else:
            cargas.pernas = request.POST.get('pernas') or 0
            cargas.bracos = request.POST.get('bracos') or 0
            cargas.peito = request.POST.get('peito') or 0
            cargas.costas = request.POST.get('costas') or 0
            cargas.save()

            # Atualiza presenças
            presencas_json = request.POST.get('presencas_json', '{}')

            try:
                presencas_data = json.loads(presencas_json)
                erros = []

                for freq_id, presente in presencas_data.items():
                    freq = CalendarioFrequencia.objects.filter(
                        id=freq_id, usuario=aluno
                    ).first()

                    if not freq:
                        continue

                    novo_estado = bool(presente)

                    # impedir marcar como ausente se tem histórico
                    if freq.presente and not novo_estado:
                        if HistoricoAtividades.objects.filter(usuario=aluno, data=freq.data).exists():
                            erros.append(freq.data.strftime('%d/%m/%Y'))
                            continue

                    freq.presente = novo_estado
                    freq.save()

                if erros:
                    messages.warning(
                        request,
                        "⚠️ Não foi possível marcar como ausente as datas: "
                        + ", ".join(erros)
                    )

                messages.success(request, "Dados salvos com sucesso!")

            except:
                messages.error(request, "Erro ao salvar calendário.")

            return redirect('TelaProf:editar_aluno', aluno_id=aluno.id)

    return render(request, 'editar_aluno.html', {
        'aluno': aluno,
        'calendario': calendario,
        'historico': historico,
        'cargas': cargas,
        'mes': mes,
        'ano': ano,
    })
