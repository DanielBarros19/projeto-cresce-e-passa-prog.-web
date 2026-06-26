from django import forms
from usuario.models import Usuario

class FormularioRegistroUsuario(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'entre com a senha',
            'class': 'form-control',
        }
    ))

    confirmar_senha = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'confirmar a senha',
            'class': 'form-control',
        }
    ))

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'nomeUsuario', 'telefone', 'endereco', 'data_nascimento', 'cpf', 'renda_mensal_casa', 'moradores_casa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seuemail@exemplo.com'}),
            'nomeUsuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu endereço'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'renda_mensal_casa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2500.00', 'step': '0.01'}),
            'moradores_casa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade de pessoas'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormularioRegistroUsuario, self).__init__(*args, **kwargs)

        if not self.is_bound:
            self.fields['renda_mensal_casa'].initial = ''
            self.fields['moradores_casa'].initial = ''

    def clean(self):
        cleaned_data = super(FormularioRegistroUsuario, self).clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if senha != confirmar_senha:
            raise forms.ValidationError('as senhas não conferem')
       
        return cleaned_data
    

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'nomeUsuario', 'email', 'telefone', 'endereco', 'data_nascimento', 'cpf', 'renda_mensal_casa', 'moradores_casa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nomeUsuario': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'renda_mensal_casa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'moradores_casa': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)

        self.fields['cpf'].widget.attrs['readonly'] = True
        self.fields['cpf'].widget.attrs['class'] += ' bg-light text-muted'
        
        