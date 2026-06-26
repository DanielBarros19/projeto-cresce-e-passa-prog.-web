from django.contrib import admin
from django.urls import include, path
from cresce_e_passa import views as principal_views
from produtos import views as produto_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', principal_views.home, name='home'), 
    path('loja/', produto_views.visualizarLoja, name='visualizarLoja'),
    path('anunciar/', produto_views.cadastrar_produto, name='cadastrar_produto'),
    path('produto/<slug:produto_slug>/', produto_views.detalhe_produto, name='detalhe_produto'),  
    path('categoria/<slug:categoria_slug>/', produto_views.visualizarLoja, name='visualizarLoja_por_categoria'),    
    path('interesse/', include('demonstrar_interesse.urls')),
    path('usuarios/', include('usuario.urls')),
    path('produtos/', include('produtos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)