from django.conf import settings
from cadastro.models import Usuario
from loginProf.models import Professor

def usuario_session(request):
    return {
        'is_usuario_logged': request.session.get('aluno_autenticado'),
        'usuario_nome': request.session.get('aluno_nome', ''),

        'is_professor_logged': request.session.get('professor_autenticado'),
        'professor_nome': request.session.get('professor_nome', ''),
    }

