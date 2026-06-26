from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizarLoja, name='visualizarLoja'),
    path('categoria/<slug:categoria_slug>/', views.visualizarLoja, name='visualizarLoja_por_categoria'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('detalhe/<slug:produto_slug>/', views.detalhe_produto, name='detalhe_produto'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    path('alternar/<int:produto_id>/', views.alternar_disponibilidade, name='alternar_disponibilidade'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('anuncio/<int:produto_id>/interessados/', views.visualizar_interessados, name='visualizar_interessados'),
    path('doar/<int:produto_id>/<int:usuario_id>/', views.doar_para_usuario, name='doar_para_usuario'),
    path('vender/<int:produto_id>/<int:usuario_id>/', views.vender_para_usuario, name='vender_para_usuario'),  # Nova rota aqui!
    path('confirmar-recebimento/<int:produto_id>/', views.confirmar_recebimento, name='confirmar_recebimento'),
]