from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from produtos.models import Produto
from .models import InteresseProduto
from django.contrib import messages

@login_required(login_url='signin')
def registrar_interesse(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # 1. Impede interesse no próprio produto
    if produto.usuario == request.user:
        messages.error(request, "Você não pode demonstrar interesse no seu próprio produto.")
        return redirect('meus_interesses') 
    
    # 2. Verifica se já existe o interesse
    ja_interessado = InteresseProduto.objects.filter(usuario=request.user, produto=produto).exists()

    if ja_interessado:
        messages.info(request, "Você já demonstrou interesse nesse produto.")
    else:
        InteresseProduto.objects.create(usuario=request.user, produto=produto)
        messages.success(request, "Interesse registrado! Vendedor/doador notificado.")

    return redirect('meus_interesses')    


@login_required(login_url='signin')
def meus_interesses(request):
    interesses = InteresseProduto.objects.filter(usuario=request.user)
    return render(request, 'usuario/meus_interesses.html', {'interesses': interesses})

@login_required(login_url='signin')
def remover_interesse(request, interesse_id):
    interesse = get_object_or_404(InteresseProduto, id=interesse_id, usuario=request.user)
    interesse.delete()
    
    messages.success(request, "Interesse removido com sucesso!")
    return redirect('meus_interesses')

@login_required(login_url='signin')
def visualizar_interessados(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario = request.user)
    interesses = InteresseProduto.objects.filter(produto=produto)

    interesses_ordenados = sorted(interesses, key=lambda x: x.usuario.renda_per_capita)
    contexto = {'produto': produto, 'interesses': interesses_ordenados,}

    return render(request, 'loja/visualizar_interessados.html', contexto)