from django.shortcuts import render, redirect, get_object_or_404
from cadastro.models import Usuario, CalendarioFrequencia, Cargas, RequisicaoExclusao
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
    cargas = {
        'pernas': 0,
        'bracos': 0,
        'peito': 0,
        'costas': 0
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
                # Se não existir registro de cargas, usa valores padrão
                cargas = {
                    'pernas': 0,
                    'bracos': 0,
                    'peito': 0,
                    'costas': 0
                }
            
            frequencias = CalendarioFrequencia.objects.filter(
                usuario=usuario
            ).order_by('data')
            
            # Organiza por mês
            if frequencias.exists():
                # Pega o intervalo de datas
                primeira_data = frequencias.first().data
                ultima_data = frequencias.last().data
                
                # Cria dicionário de frequências para lookup rápido
                freq_dict = {f.data: f.presente for f in frequencias}
                
                # Gera calendário mês a mês
                data_atual = primeira_data.replace(day=1)
                while data_atual <= ultima_data:
                    ano = data_atual.year
                    mes = data_atual.month
                    dias_no_mes = monthrange(ano, mes)[1]
                    
                    # Nome do mês em português
                    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
                    nome_mes = meses_pt[mes - 1]
                    
                    # Primeiro dia da semana (0=segunda, 6=domingo)
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
                    
                    # Próximo mês
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
        'cargas': cargas
    })

def nutricao(request):
    return render(request, 'nutrição.html', {})

def configuracoes(request):
    usuario_id = request.session.get('usuario_id')
    nome = request.session.get('nome_usuario_completo', 'Usuário')

    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

    # ===========================
    #         POST
    # ===========================
    if request.method == 'POST':
        if usuario:
            # Requisição de exclusão de conta
            if 'requisitar_exclusao' in request.POST:
                motivo = request.POST.get('motivo_exclusao', '')
                
                # Verifica se já existe requisição pendente
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
            
            # Atualização de configurações normais
            observacoes = request.POST.get('observacoes', '')
            email = request.POST.get('email', '')
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')

            usuario.observacoes = observacoes

            # Validação do email
            try:
                validate_email(email)
                usuario.email = email
            except ValidationError:
                messages.warning(request, "E-mail inválido. Mantendo o e-mail anterior.")

            # Validação da senha
            if nova_senha:
                if nova_senha == confirmar_senha:
                    usuario.senha = nova_senha
                    messages.success(request, "Senha atualizada com sucesso.")
                else:
                    messages.error(request, "As senhas não coincidem. A senha não foi alterada.")

            usuario.save()
            messages.success(request, "Configurações salvas com sucesso.")

        return redirect('TelaAluno:configuracoes')

    # ==========================
    #          GET
    # ==========================
    # Verifica se há requisição pendente
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