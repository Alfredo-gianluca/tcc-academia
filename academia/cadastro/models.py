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
        return '{self.aluno.nome} - {self.data_frequencia}'
