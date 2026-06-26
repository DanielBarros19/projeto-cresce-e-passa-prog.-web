import re
import urllib.parse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, FloatField, Case, When
from demonstrar_interesse.models import InteresseProduto
from produtos.models import Produto
from categoria.models import Categoria
from .forms import ProdutoForm

User = get_user_model()


def visualizarLoja(request, categoria_slug=None):
    categorias = None
    produtos = None

    if categoria_slug is not None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        produtos = Produto.objects.filter(produto_categoria=categorias, produto_esta_disponivel=True)
    else:
        produtos = Produto.objects.filter(produto_esta_disponivel=True)

    # Barra de pesquisa filtra por palavra-chave
    keyword = request.GET.get('keyword')
    if keyword:
        produtos = produtos.filter(produto_nome__icontains=keyword)

    # Filtro da loja por Tipo (Doação/Venda)
    tipo = request.GET.get('tipo')
    if tipo:
        produtos = produtos.filter(produto_tipo=tipo)

    # 4. Filtro de Faixa de Preço
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    try:
        if preco_min and preco_min.isdigit():
            produtos = produtos.filter(produto_preco__gte=int(preco_min))
        
        if preco_max and preco_max.isdigit():
            if int(preco_max) < 9999:  # Evita filtrar o teto se for a opção "Qualquer valor"
                produtos = produtos.filter(produto_preco__lte=int(preco_max))
    except ValueError:
        pass

    # 5. Ordenação, filtrando os mais recentes primeiro
    produtos = produtos.order_by('-produto_criado_em')

    context = {
        'produtos': produtos,
    }
    return render(request, 'loja/loja.html', context)

@login_required(login_url='signin')
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            
            if request.user.is_authenticated:
                produto.usuario = request.user
                
            produto.slug = f"{slugify(produto.produto_nome)}-{request.user.id}"
            produto.save()
            return redirect('meus_anuncios')
    else:
        form = ProdutoForm()
    listarCategorias = Categoria.objects.all()    

    return render(request, 'produtos/cadastrar_produto.html', {'form': form, 'listaCategorias': listarCategorias, 'titulo_pagina': 'Cadastrar Anúncio'})


def detalhe_produto(request, produto_slug):
    produto = get_object_or_404(Produto, slug=produto_slug)

    context = {
        'produto': produto,
    }
    return render(request, 'loja/detalhe_produto.html', context)


@login_required
def meus_anuncios(request):
    produtos = Produto.objects.filter(usuario=request.user).order_by('-produto_criado_em')
    return render(request, 'produtos/meus_anuncios.html', {'produtos': produtos})


@login_required
def alternar_disponibilidade(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    produto.produto_esta_disponivel = not produto.produto_esta_disponivel
    produto.save()
    return redirect('meus_anuncios')


@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            produto_editado = form.save(commit=False)
            produto_editado.slug = slugify(produto_editado.produto_nome)
            produto_editado.save()
            return redirect('meus_anuncios')
    else:
        form = ProdutoForm(instance=produto)
        
    return render(request, 'produtos/cadastrar_produto.html', { 'form': form, 'produto': produto, 'titulo_pagina': 'Editar Anúncio'})


@login_required
def visualizar_interessados(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    interesses_registrados = InteresseProduto.objects.filter(produto=produto)
    
    if produto.produto_tipo == 'DOACAO':
        interesses_registrados = interesses_registrados.annotate(
            renda_per_capita_db=ExpressionWrapper(
                Case(
                    When(usuario__moradores_casa__gt=0, then=F('usuario__renda_mensal_casa') / F('usuario__moradores_casa')),
                    default=F('usuario__renda_mensal_casa'),
                ),
                output_field=FloatField()
            )
        ).order_by('renda_per_capita_db')
    else:
        interesses_registrados = interesses_registrados.order_by('data_interesse')

    context = {
        'produto': produto,
        'interesses_registrados': interesses_registrados,
    }
    
    if produto.produto_tipo == 'DOACAO':
        return render(request, 'produtos/interessados_doacao.html', context)
    else:
        return render(request, 'produtos/interessados_venda.html', context)


@login_required
def doar_para_usuario(request, produto_id, usuario_id):

    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    destinatario = get_object_or_404(User, id=usuario_id)
    
    produto.donatario = destinatario
    produto.produto_esta_disponivel = False 
    produto.doacao_confirmada_doador = True
    
    if produto.produto_tipo == 'VENDA':
        produto.doacao_confirmada_recebedor = True 
        produto.save()
        nome_comprador = getattr(destinatario, 'username', getattr(destinatario, 'nome', 'Usuário'))
        messages.success(request, f"Venda do produto '{produto.produto_nome}' concluída com sucesso para {nome_comprador}!")
        return redirect('meus_anuncios')
        
    produto.save()
    
    nome_exibicao = getattr(destinatario, 'username', getattr(destinatario, 'nome', 'Usuário'))
    telefone = getattr(destinatario, 'telefone', None)
    
    if telefone:
        telefone_limpo = re.sub(r'\D', '', str(telefone))
        mensagem_wp = f"Olá, vi que você demonstrou interesse no meu anúncio '{produto.produto_nome}' e escolhi você para a doação!"
        mensagem_codificada = urllib.parse.quote(mensagem_wp)
        link_whatsapp = f"https://wa.me/55{telefone_limpo}?text={mensagem_codificada}"
        
        messages.success(request, f"Interesse confirmado! Entre em contato para combinar clicando aqui: {link_whatsapp}")
    else:
        messages.success(request, f"Confirmação realizada com sucesso para {nome_exibicao}! Aguardando o retorno dele.")
        
    return redirect('meus_anuncios')


@login_required
def vender_para_usuario(request, produto_id, usuario_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user, produto_tipo='VENDA')
    comprador = get_object_or_404(User, id=usuario_id)
    
    produto.donatario = comprador
    produto.produto_esta_disponivel = False 
    produto.doacao_confirmada_doador = True
    produto.doacao_confirmada_recebedor = True 
    produto.save()
    
    nome_comprador = getattr(comprador, 'username', getattr(comprador, 'nome', 'Usuário'))
    messages.success(request, f"Venda do produto '{produto.produto_nome}' concluída com sucesso para {nome_comprador}!")
    
    return redirect('meus_anuncios')


@login_required
def confirmar_recebimento(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, donatario=request.user)
    produto.doacao_confirmada_recebedor = True
    produto.save()
    
    nome_doador = getattr(produto.usuario, 'username', getattr(produto.usuario, 'nome', 'Doador'))
    messages.success(request, f"Você confirmou que recebeu o produto de {nome_doador}!")
    return redirect('meus_interesses')