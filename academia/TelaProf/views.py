import json
from django.shortcuts import render, get_object_or_404, redirect
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao, HistoricoAtividades, Ficha
from utils.decorators import login_required
from django.contrib import messages
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.http import HttpResponse

@login_required
def lista_alunos(request):
    # Texto digitado na barra de busca
    search = request.GET.get('search', '')

    # Filtragem automática
    if search:
        alunos = Usuario.objects.filter(nome_completo__icontains=search)
    else:
        alunos = Usuario.objects.all()

    requisicoes = RequisicaoExclusao.objects.filter(status='pendente').select_related('usuario')

    # Aba ativa
    aba_ativa = request.GET.get('aba', 'alunos')

    # POSTs da página
    if request.method == 'POST':

        # APROVAR REQUISIÇÃO
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

        # REJEITAR REQUISIÇÃO
        elif 'rejeitar_requisicao' in request.POST:
            requisicao_id = request.POST.get('requisicao_id')
            requisicao = get_object_or_404(RequisicaoExclusao, id=requisicao_id)
            
            requisicao.status = 'rejeitada'
            requisicao.save()
            
            messages.info(request, f"Requisição de {requisicao.usuario.nome_completo} foi rejeitada.")
            return redirect('TelaProf:lista_alunos')

        # EXCLUIR ALUNO
        elif 'delete_aluno' in request.POST:
            aluno_id = request.POST.get('aluno_id')
            aluno = get_object_or_404(Usuario, id=aluno_id)
            nome = aluno.nome_completo

            aluno.delete()

            messages.success(request, f"Aluno {nome} foi excluído com sucesso.")
            return redirect('TelaProf:lista_alunos')

    return render(request, 'lista_alunos.html', {
        'alunos': alunos,
        'requisicoes': requisicoes,
        'aba_ativa': aba_ativa,
        'search': search,
    })


@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id)
    calendario = CalendarioFrequencia.objects.filter(usuario=aluno).order_by('-data')
    historico = HistoricoAtividades.objects.filter(usuario=aluno).order_by('-data')
    cargas, _ = Cargas.objects.get_or_create(usuario=aluno)
    ficha , _ = Ficha.objects.get_or_create(usuario=aluno)

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
            ficha.supino_reto = request.POST.get('supino_reto') or 0
            ficha.supino_inclinado = request.POST.get('supino_inclinado') or 0
            ficha.crucifixo = request.POST.get('crucifixo') or 0
            ficha.remada_curvada = request.POST.get('remada_curvada') or 0
            ficha.puxada_na_barra = request.POST.get('puxada_na_barra') or 0
            ficha.agachamento_livre = request.POST.get('agachamento_livre') or 0
            ficha.leg_press = request.POST.get('leg_press') or 0
            ficha.desenvolvimento = request.POST.get('desenvolvimento') or 0
            ficha.rosca_direta = request.POST.get('rosca_direta') or 0
            ficha.triceps_testa = request.POST.get('triceps_testa') or 0
            ficha.save()

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
        'ficha': ficha,
        'mes': mes,
        'ano': ano,
    })

def gerar_pdf_aluno(request, aluno_id):
    aluno = get_object_or_404(Usuario, id=aluno_id)

    # Configurações iniciais
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Ficha_{aluno.nome_completo}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Título
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(largura / 2, altura - 50, "Ficha do Aluno")

    pdf.setFont("Helvetica", 10)
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.drawRightString(largura - 40, altura - 70, f"Gerado em: {data_geracao}")

    # Informações
    pdf.setFont("Helvetica", 12)
    y = altura - 100

    generos_completos = {
        "M": "Masculino",
        "F": "Feminino",
        "O": "Outro",
    }

    dados = [
        ("Nome completo:", aluno.nome_completo),
        ("Email:", aluno.email),
        ("Telefone:", aluno.telefone if hasattr(aluno, "telefone") else "—"),
        ("Data de nascimento:", aluno.data_nascimento.strftime("%d/%m/%Y") if hasattr(aluno, "data_nascimento") else "—"),
        ("Observações:", aluno.observacoes or "Nenhuma"),
        ("Gênero:", generos_completos.get(aluno.genero, "—")),
        
    ]

    for label, valor in dados:
        pdf.drawString(50, y, f"{label} {valor}")
        y -= 25

    # Se quiser adicionar cargas (caso existam)
    try:
        cargas = Cargas.objects.get(usuario=aluno)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y - 10, "Cargas:")
        y -= 40

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Pernas: {cargas.pernas} kg")
        pdf.drawString(250, y, f"Braços: {cargas.bracos} kg")
        y -= 20
        pdf.drawString(50, y, f"Peito: {cargas.peito} kg")
        pdf.drawString(250, y, f"Costas: {cargas.costas} kg")
        y -= 30
    except Cargas.DoesNotExist:
        pass

    # Se quiser incluir Ficha de Treino
    try:
        ficha = Ficha.objects.get(usuario=aluno)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y - 10, "Ficha de Treino:")
        y -= 40
        pdf.setFont("Helvetica", 12)

        exercicios = [
            ("Supino Reto", ficha.supino_reto),
            ("Supino Inclinado", ficha.supino_inclinado),
            ("Crucifixo", ficha.crucifixo),
            ("Remada Curvada", ficha.remada_curvada),
            ("Puxada na Barra", ficha.puxada_na_barra),
            ("Agachamento Livre", ficha.agachamento_livre),
            ("Leg Press", ficha.leg_press),
            ("Desenvolvimento", ficha.desenvolvimento),
            ("Rosca Direta", ficha.rosca_direta),
            ("Tríceps Testa", ficha.triceps_testa),
        ]

        for ex, carga in exercicios:
            pdf.drawString(50, y, f"{ex}: {carga} kg")
            y -= 20

    except Ficha.DoesNotExist:
        pass

    pdf.showPage()
    pdf.save()

    return response
