from django.contrib import admin
from .models import Usuario, CalendarioFrequencia, Cargas, HistoricoAtividades

admin.site.register(Usuario)
admin.site.register(CalendarioFrequencia)
admin.site.register(Cargas)
admin.site.register(HistoricoAtividades)