from functools import wraps
from django.shortcuts import redirect

def aluno_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('aluno_autenticado'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Mudou aqui! ↓↓↓
        if not request.session.get('professor_autenticado'):
            return redirect('loginProf:loginprof')
        return view_func(request, *args, **kwargs)
    return wrapper