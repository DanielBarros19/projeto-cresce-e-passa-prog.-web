from django.http import HttpResponse
from django.shortcuts import render
from produtos.models import Produto 

def home(request):
    doacoes = Produto.objects.filter(produto_tipo='DOACAO', produto_esta_disponivel=True).order_by('-produto_criado_em')[:4]
    
    vendas = Produto.objects.filter(produto_tipo='VENDA', produto_esta_disponivel=True).order_by('-produto_criado_em')[:4]

    context = {
        'doacoes': doacoes,
        'vendas': vendas,
    }
    
    return render(request, 'home.html', context)