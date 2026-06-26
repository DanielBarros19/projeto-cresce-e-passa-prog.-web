from django.db import models
from categoria.models import Categoria
from django.conf import settings

class Produto(models.Model):
    TIPO_CHOICES = (
        ('VENDA', 'venda'),
        ('DOACAO', 'doação')
    )

    produto_nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    produto_descricao = models.TextField(max_length=300, blank=True)
    produto_preco = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True, blank=True)
    produto_imagens = models.ImageField(upload_to='fotos/produto')
    produto_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) 
    produto_tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='VENDA')
    produto_esta_disponivel = models.BooleanField(default=True)
    produto_criado_em = models.DateField(auto_now_add=True)
    produto_modificado_em = models.DateField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='doacoes_recebidas')
    doacao_confirmada_doador = models.BooleanField(default=False)
    doacao_confirmada_recebedor = models.BooleanField(default=False)

    def obter_status(self):
        if not self.produto_esta_disponivel and (self.doacao_confirmada_doador and self.doacao_confirmada_recebedor or self.donatario):
            return 'FINALIZADO'
        
        elif self.donatario or self.doacao_confirmada_doador or self.doacao_confirmada_recebedor:
            return 'EM_ANDAMENTO'
        
        return 'DISPONIVEL'

    def __str__(self):
        return self.produto_nome

    def save(self, *args, **kwargs):
        if self.produto_tipo == 'DOACAO':
            self.produto_preco = 0.00
        super(Produto, self).save(*args, **kwargs)