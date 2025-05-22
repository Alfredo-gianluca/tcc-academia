from django.db import models

class Membro(models.Model):
  nome = models.CharField(max_length=255)
  sobrenome = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  data_nascimento = models.DateField(null=True, blank=True)
  telefone = models.CharField(max_length=20, blank=True)
  data_cadastro = models.DateTimeField(auto_now_add=True)
  peso = models.FloatField(null=True, blank=True)

  def __str__(self):
    return f"{self.nome} {self.sobrenome}"
    