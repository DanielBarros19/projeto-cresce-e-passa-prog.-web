from django.db import models
from django.conf import settings
from produtos.models import Produto

class InteresseProduto(models.Model):
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário Interessado")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    data_interesse = models.DateTimeField(auto_now_add=True,verbose_name="Data do Interesse")

    def __str__(self):
        return f"{self.usuario.nome} interessado em {self.produto.produto_nome}"
    
    class Meta:
        verbose_name = "Interesse"
        verbose_name_plural = "Interesses"