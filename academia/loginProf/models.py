from django.db import models

class Professor(models.Model):
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_completo

# Create your models here.
