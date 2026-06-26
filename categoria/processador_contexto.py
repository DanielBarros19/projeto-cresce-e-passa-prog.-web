from categoria.models import Categoria

def listarCategorias(request):
    categorias = Categoria.objects.all()
    return {'listaCategorias':categorias}