from django.urls import path
from . import views

urlpatterns= [

    path('registrar/<int:produto_id>/', views.registrar_interesse, name='registrar_interesse'),
    path('meus_interesses/', views.meus_interesses, name='meus_interesses'),
    path('meus-interesses/remover/<int:interesse_id>/', views.remover_interesse, name='remover_interesse'),
    path('produto/<int:produto_id>/interessados/', views.visualizar_interessados, name='visualizar_interessados'),
]