from django.contrib import admin
from .models import Produto  # Importa o modelo Produto que está na mesma pasta

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Colunas listadas na tabela do painel admin
    list_display = (
        'produto_nome', 
        'produto_tipo', 
        'produto_preco', 
        'usuario', 
        'donatario', 
        'produto_esta_disponivel', 
        'produto_criado_em'
    )
    
    list_filter = ('produto_tipo', 'produto_esta_disponivel', 'doacao_confirmada_doador', 'doacao_confirmada_recebedor')
    
    search_fields = ('produto_nome', 'usuario__username', 'donatario__username')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'produto_nome', 'slug', 'produto_categoria', 'produto_imagens')
        }),
        ('Valores e Tipo', {
            'fields': ('produto_tipo', 'produto_preco', 'produto_esta_disponivel')
        }),
        ('Fluxo de Doação', {
            'fields': ('donatario', 'doacao_confirmada_doador', 'doacao_confirmada_recebedor')
        }),
    )
    
    prepopulated_fields = {'slug': ('produto_nome',)}