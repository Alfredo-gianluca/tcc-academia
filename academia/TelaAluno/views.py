from django.shortcuts import render, redirect, get_object_or_404
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao, HistoricoAtividades, Ficha
from datetime import datetime
from calendar import monthrange
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from utils.decorators import aluno_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@aluno_required
def TelaAluno(request):
    # ✅ CORRIGIDO: Usar 'aluno_nome' e 'aluno_id'
    nome = request.session.get('aluno_nome', 'Usuário')
    usuario_id = request.session.get('aluno_id')
    
    frequencias = []
    calendario_dados = []
    historico_atividades = []
    cargas = {
        'pernas': 0,
        'bracos': 0,
        'peito': 0,
        'costas': 0
    }
    ficha = {
        'supino_reto': 0,
        'supino_inclinado': 0,
        'crucifixo': 0,
        'remada_curvada': 0,
        'puxada_na_barra': 0,
        'agachamento_livre': 0,
        'leg_press': 0,
        'desenvolvimento': 0,
        'rosca_direta': 0,
        'triceps_testa': 0,
    }

    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Busca as cargas do usuário no model Cargas
            try:
                cargas_obj = Cargas.objects.get(usuario=usuario)
                cargas = {
                    'pernas': cargas_obj.pernas,
                    'bracos': cargas_obj.bracos,
                    'peito': cargas_obj.peito,
                    'costas': cargas_obj.costas
                }
            except Cargas.DoesNotExist:
                cargas = {
                    'pernas': 0,
                    'bracos': 0,
                    'peito': 0,
                    'costas': 0
                }

            try:
                ficha_obj = Ficha.objects.get(usuario=usuario)
                ficha = {
                    'supino_reto': ficha_obj.supino_reto,
                    'supino_inclinado': ficha_obj.supino_inclinado,
                    'crucifixo': ficha_obj.crucifixo,
                    'remada_curvada': ficha_obj.remada_curvada,
                    'puxada_na_barra': ficha_obj.puxada_na_barra,
                    'agachamento_livre': ficha_obj.agachamento_livre,
                    'leg_press': ficha_obj.leg_press,
                    'desenvolvimento': ficha_obj.desenvolvimento,
                    'rosca_direta': ficha_obj.rosca_direta,
                    'triceps_testa': ficha_obj.triceps_testa,
                }
            except Ficha.DoesNotExist:
                ficha = {
                    'supino_reto': 0,
                    'supino_inclinado': 0,
                    'crucifixo': 0,
                    'remada_curvada': 0,
                    'puxada_na_barra': 0,
                    'agachamento_livre': 0,
                    'leg_press': 0,
                    'desenvolvimento': 0,
                    'rosca_direta': 0,
                    'triceps_testa': 0,
                }    
            
            # Busca histórico de atividades (ordenado por data decrescente)
            historico_atividades = HistoricoAtividades.objects.filter(
                usuario=usuario
            ).order_by('-data')[:3]  # Últimas 3 atividades
            
            frequencias = CalendarioFrequencia.objects.filter(
                usuario=usuario
            ).order_by('data')
            
            # Organiza por mês
            if frequencias.exists():
                primeira_data = frequencias.first().data
                ultima_data = frequencias.last().data
                
                freq_dict = {f.data: f.presente for f in frequencias}
                
                data_atual = primeira_data.replace(day=1)
                while data_atual <= ultima_data:
                    ano = data_atual.year
                    mes = data_atual.month
                    dias_no_mes = monthrange(ano, mes)[1]
                    
                    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
                    nome_mes = meses_pt[mes - 1]
                    
                    primeiro_dia_semana = datetime(ano, mes, 1).weekday()
                    
                    dias_mes = []
                    for dia in range(1, dias_no_mes + 1):
                        data_dia = datetime(ano, mes, dia).date()
                        presente = freq_dict.get(data_dia)
                        dias_mes.append({
                            'dia': dia,
                            'presente': presente,
                            'tem_registro': data_dia in freq_dict
                        })
                    
                    calendario_dados.append({
                        'mes': nome_mes,
                        'ano': ano,
                        'dias': dias_mes,
                        'offset': primeiro_dia_semana
                    })
                    
                    if mes == 12:
                        data_atual = datetime(ano + 1, 1, 1).date()
                    else:
                        data_atual = datetime(ano, mes + 1, 1).date()
                        
        except Usuario.DoesNotExist:
            usuario = None
    else:
        usuario = None

    return render(request, 'telainicial.html', {
        'centralizar_logo': False,
        'nome_usuario': nome,
        'frequencias': frequencias,
        'calendario_dados': calendario_dados,
        'cargas': cargas,
        'historico_atividades': historico_atividades,
        'ficha': ficha,
        'usuario': usuario,
    })

@aluno_required
def nutricao(request):
    return render(request, 'nutrição.html', {})

@aluno_required
def configuracoes(request):
    usuario_id = request.session.get('aluno_id')
    nome = request.session.get('aluno_nome', 'Usuário')

    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

    if request.method == 'POST':
        if usuario:

            # --- REQUISIÇÃO DE EXCLUSÃO ---
            if 'requisitar_exclusao' in request.POST:
                motivo = request.POST.get('motivo_exclusao', '')
                
                requisicao_existente = RequisicaoExclusao.objects.filter(
                    usuario=usuario,
                    status='pendente'
                ).exists()
                
                if requisicao_existente:
                    messages.warning(request, "Você já possui uma requisição de exclusão pendente.")
                else:
                    RequisicaoExclusao.objects.create(
                        usuario=usuario,
                        motivo=motivo
                    )
                    messages.success(request, "Requisição de exclusão enviada ao professor com sucesso!")
                
                return redirect('TelaAluno:configuracoes')

            # --- ATUALIZAÇÃO DE DADOS ---
            observacoes = request.POST.get('observacoes', '')
            email = request.POST.get('email', '')
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')
            fotoperfil = request.POST.get('fotoperfil')

            usuario.observacoes = observacoes

            # Atualizar e-mail
            try:
                validate_email(email)
                usuario.email = email
            except ValidationError:
                messages.warning(request, "E-mail inválido. Mantendo o e-mail anterior.")
            

            # Atualizar senha
            if nova_senha:

                # Verifica se as senhas coincidem
                if nova_senha != confirmar_senha:
                    messages.error(request, "As senhas não coincidem. Tente novamente.")
                    return redirect('TelaAluno:configuracoes')

                # Valida tamanho mínimo
                if len(nova_senha) < 8:
                    messages.error(request, "A senha deve ter no mínimo 8 caracteres.")
                    return redirect('TelaAluno:configuracoes')

                # Verifica letra maiúscula
                if not any(c.isupper() for c in nova_senha):
                    messages.error(request, "A senha deve conter pelo menos uma letra maiúscula.")
                    return redirect('TelaAluno:configuracoes')

                # Verifica número
                if not any(c.isdigit() for c in nova_senha):
                    messages.error(request, "A senha deve conter pelo menos um número.")
                    return redirect('TelaAluno:configuracoes')

                # Se passou por todas as validações, atualiza
                usuario.senha = nova_senha
                messages.success(request, "Senha atualizada com sucesso.")
        

            # --- ATUALIZA A FOTO DE PERFIL ---
            if 'fotoperfil' in request.FILES:
                usuario.fotoperfil = request.FILES['fotoperfil']
                messages.success(request, "Foto de perfil atualizada!")

            usuario.save()
            messages.success(request, "Configurações salvas com sucesso.")

        return redirect('TelaAluno:configuracoes')

    # Exibir página
    requisicao_pendente = None
    if usuario:
        requisicao_pendente = RequisicaoExclusao.objects.filter(
            usuario=usuario,
            status='pendente'
        ).first()
    
    return render(request, 'configurações.html', {
        'usuario': usuario,
        'aluno': usuario,
        'nome_usuario': nome,
        'requisicao_pendente': requisicao_pendente,
    })

@aluno_required
def treinos(request):
    return render(request, 'treinos.html', {})

@aluno_required
def historico_completo(request):
    # ✅ CORRIGIDO
    usuario_id = request.session.get('aluno_id')
    historico_atividades = []

    if not usuario_id:
        return redirect('TelaAluno:TelaAluno')

    usuario = Usuario.objects.get(id=usuario_id)

    historico = HistoricoAtividades.objects.filter(
        usuario=usuario
    ).order_by('-data')

    return render(request, 'historico.html', {
        'historico': historico,
        'nome_usuario': request.session.get('aluno_nome', 'Usuário')  # ✅ Corrigido
    })

@aluno_required
def gerar_pdf(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    # Configurações iniciais
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Ficha_{usuario.nome_completo}.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Título
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(largura / 2, altura - 50, "Ficha do Aluno")

    # Data de geração
    pdf.setFont("Helvetica", 10)
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.drawRightString(largura - 40, altura - 70, f"Gerado em: {data_geracao}")

    # Informações do aluno
    pdf.setFont("Helvetica", 12)
    y = altura - 100

    # Gênero por extenso
    generos_completos = {
        "M": "Masculino",
        "F": "Feminino",
        "O": "Outro",
    }

    dados = [
        ("Nome completo:", usuario.nome_completo),
        ("Email:", usuario.email),
        ("Telefone:", getattr(usuario, "telefone", "—")),
        ("Data de nascimento:", usuario.data_nascimento.strftime("%d/%m/%Y") if getattr(usuario, "data_nascimento", None) else "—"),
        ("Observações:", usuario.observacoes or "Nenhuma"),
        ("Gênero:", generos_completos.get(usuario.genero, "—")),
    ]

    for label, valor in dados:
        pdf.drawString(50, y, f"{label} {valor}")
        y -= 25

    # Cargas
    try:
        cargas = Cargas.objects.get(usuario=usuario)

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

    # Ficha de treino
    try:
        ficha = Ficha.objects.get(usuario=usuario)

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