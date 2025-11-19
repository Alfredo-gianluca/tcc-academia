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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    Treino = models.TextField()
    qtdexercicios = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.usuario.nome_completo} - {self.data}'

class RequisicaoExclusao(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_requisicao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aprovada', 'Aprovada'), ('recusada', 'Recusada')], default='pendente')

    def __str__(self):
        return f"Requisição de {self.aluno.nome_completo} em {self.data_requisicao} - {self.status}"
