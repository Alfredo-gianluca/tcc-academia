from django.db import models


class Usuario(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não dizer'),
    ]

    nome_completo = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    observacoes = models.TextField(blank=True)
    
    fotoperfil = models.ImageField(
        upload_to='fotos_perfil/',
        null=True,
        blank=True,
        verbose_name='Foto de Perfil'
    )
    
    def get_foto_perfil(self):
        from django.templatetags.static import static
        import os
        if self.fotoperfil and hasattr(self.fotoperfil, 'path') and os.path.isfile(self.fotoperfil.path):
            return self.fotoperfil.url
        return static('img/default.jpg')

    def __str__(self):
        return self.nome_completo

class CalendarioFrequencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.data}'

class Cargas(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pernas = models.IntegerField()
    bracos = models.IntegerField()
    costas = models.IntegerField()
    peito = models.IntegerField()
    def __str__(self):
        return f'{self.usuario.nome_completo} - Cargas'
    
class HistoricoAtividades(models.Model):
    treino_choices = [
        ('Pernas', 'Treino de pernas'),
        ('Braços', 'Treino de braços'),
        ('Costas', 'Treino de costas'),
        ('Peito', 'Treino de peito'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField()
    Treino = models.CharField(max_length=6, choices= treino_choices)
    qtdexercicios = models.CharField(max_length=20)
    cargas = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.data}'

class RequisicaoExclusao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='requisicoes_exclusao')
    data_requisicao = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('aprovada', 'Aprovada'),
            ('rejeitada', 'Rejeitada')
        ],
        default='pendente'
    )
    
    class Meta:
        verbose_name = 'Requisição de Exclusão'
        verbose_name_plural = 'Requisições de Exclusão'
        ordering = ['-data_requisicao']
    
    def __str__(self):
        return f"Requisição de {self.usuario.nome_completo} - {self.status}"

class Ficha(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    supino_reto = models.IntegerField(default=0)
    supino_inclinado = models.IntegerField(default=0)
    crucifixo = models.IntegerField(default=0)
    remada_curvada = models.IntegerField(default=0)
    puxada_na_barra = models.IntegerField(default=0)
    agachamento_livre = models.IntegerField(default=0)
    leg_press = models.IntegerField(default=0)
    desenvolvimento = models.IntegerField(default=0)
    rosca_direta = models.IntegerField(default=0)
    triceps_testa = models.IntegerField(default=0)

    def __str__(self):
        return f'Ficha de {self.usuario.nome_completo}'
