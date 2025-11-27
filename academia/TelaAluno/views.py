from django.shortcuts import render, redirect, get_object_or_404
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao, HistoricoAtividades, Ficha
from datetime import datetime
from calendar import monthrange
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages

def TelaAluno(request):
    nome = request.session.get('nome_usuario_completo', 'Usuário')
    usuario_id = request.session.get('usuario_id')
    frequencias = []
    calendario_dados = []
    historico_atividades = []
    cargas = {
        'pernas': 0,
        'bracos': 0,
        'peito': 0,
        'costas': 0
    }
    ficha= {
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
        'historico_atividades': historico_atividades
    })

def nutricao(request):
    return render(request, 'nutrição.html', {})

def configuracoes(request):
    usuario_id = request.session.get('usuario_id')
    nome = request.session.get('nome_usuario_completo', 'Usuário')

    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

    if request.method == 'POST':
        if usuario:
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
            
            observacoes = request.POST.get('observacoes', '')
            email = request.POST.get('email', '')
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')

            usuario.observacoes = observacoes

            try:
                validate_email(email)
                usuario.email = email
            except ValidationError:
                messages.warning(request, "E-mail inválido. Mantendo o e-mail anterior.")

            if nova_senha:
                if nova_senha == confirmar_senha:
                    usuario.senha = nova_senha
                    messages.success(request, "Senha atualizada com sucesso.")
                else:
                    messages.error(request, "As senhas não coincidem. A senha não foi alterada.")

            usuario.save()
            messages.success(request, "Configurações salvas com sucesso.")

        return redirect('TelaAluno:configuracoes')

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

def treinos(request):
    return render(request, 'treinos.html', {})

def historico_completo(request):
    usuario_id = request.session.get('usuario_id')
    historico_atividades = []

    if not usuario_id:
        return redirect('TelaAluno:TelaAluno')

    usuario = Usuario.objects.get(id=usuario_id)

    historico = HistoricoAtividades.objects.filter(
        usuario=usuario
    ).order_by('-data')

    return render(request, 'historico.html', {
        'historico': historico,
        'nome_usuario': request.session.get('nome_usuario_completo', 'Usuário')
    })