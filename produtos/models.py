from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    estoque = models.IntegerField()

    def __str__(self):
        return f"{self.nome} - Estoque: {self.estoque}"
    