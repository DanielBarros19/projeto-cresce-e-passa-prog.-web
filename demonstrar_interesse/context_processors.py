from .models import InteresseProduto

def contador_interesses(request):
    if request.user.is_authenticated:
        quantidade = InteresseProduto.objects.filter(usuario=request.user).count()
    else:
        quantidade = 0
        
    return {'quantidade_interesses': quantidade}