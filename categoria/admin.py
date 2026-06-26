from django.contrib import admin
from categoria.models import Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria_nome' ,)

admin.site.register(Categoria, CategoriaAdmin)
