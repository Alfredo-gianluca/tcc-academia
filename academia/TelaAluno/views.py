from django.shortcuts import render
from cadastro.models import Usuario, CalendarioFrequencia, Cargas
from datetime import datetime
from calendar import monthrange

def TelaAluno(request):
    nome = request.session.get('nome_usuario_completo', 'Usuário')
    usuario_id = request.session.get('usuario_id')
    
    # TESTE TEMPORÁRIO - remova depois de ajustar o login
    if not request.session.get('usuario_id'):
        primeiro_usuario = Usuario.objects.first()
        if primeiro_usuario:
            request.session['usuario_id'] = primeiro_usuario.id
    
    usuario_id = request.session.get('usuario_id')
    frequencias = []
    calendario_dados = []
    cargas = {
        'pernas': 0,
        'bracos': 0,
        'peito': 0,
        'costas': 0
    }
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
        'calendario_dados': calendario_dados
    })

def nutricao(request):
    return render(request, 'nutrição.html', {})

def configuracoes(request):
    return render(request, 'configurações.html', {})

def treinos(request):
    return render(request, 'treinos.html', {})


def configuracoes(request):
    return render(request, 'configurações.html', {})

def treinos(request):
    return render(request, 'treinos.html', {})
