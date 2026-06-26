from django.urls import path    
from usuario import views   

urlpatterns= [
    path('registrar/', views.registrarUsuario, name='register'),
    path('login/', views.autenticarUsuario, name='signin'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('logout/', views.logout_usuario, name='logout'),
]