from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['produto_nome', 'produto_descricao', 'produto_preco', 'produto_imagens', 'produto_categoria', 'produto_tipo']

        widgets = {
            'produto_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: berço americano'}),
            'produto_descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'produto_preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'produto_categoria': forms.Select(attrs={'class': 'form-control'}),
            'produto_tipo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
            super(ProdutoForm, self).__init__(*args, **kwargs)
            self.fields['produto_imagens'].required = False