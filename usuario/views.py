from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout 
from usuario.forms import FormularioRegistroUsuario, EditarPerfilForm
from usuario.models import Usuario

def registrarUsuario(request):
    if request.method == 'POST':
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']
            nomeUsuario = form.cleaned_data['nomeUsuario']
            email = form.cleaned_data['email']
            endereco = form.cleaned_data['endereco']
            data_nascimento = form.cleaned_data['data_nascimento']
            cpf = form.cleaned_data['cpf']
            senha = form.cleaned_data['senha']
            renda_mensal_casa = form.cleaned_data.get('renda_mensal_casa', 0.00)
            moradores_casa = form.cleaned_data.get('moradores_casa', 1)
            
            usuario = Usuario.objects.create_user(
                nome=nome, 
                email=email, 
                nomeUsuario=nomeUsuario, 
                telefone=telefone, 
                endereco=endereco,
                password=senha,
                data_nascimento=data_nascimento,
                cpf=cpf,
                renda_mensal_casa=renda_mensal_casa,
                moradores_casa=moradores_casa
            )
            
            messages.success(request, "Cadastro realizado com sucesso! Faça o seu login.")
            return redirect('signin')
    else:
        form = FormularioRegistroUsuario()

    return render(request, 'usuario/registrar.html', {'form': form})

def autenticarUsuario(request):
    if request.method == 'POST':
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('senha')

        usuario = authenticate(request, username=email_digitado, password=senha_digitada)

        if usuario is not None:
            django_login(request, usuario)
            messages.success(request, f"Bem-vindo de volta, {usuario.nome}!")
            return redirect('home')  # Te manda para a página inicial logado
        else:
            messages.error(request, "E-mail ou senha incorretos. Tente novamente.")
            return redirect('signin')

    return render(request, 'usuario/autenticar.html')

@login_required(login_url='signin')
def perfil_usuario(request):
    usuario_atual = request.user

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario_atual)
        form.data = form.data.copy()
        form.data['cpf'] = usuario_atual.cpf
         
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_usuario')
    else:
        form = EditarPerfilForm(instance=request.user)
        
    return render(request, 'usuario/perfil.html', {'form': form})

def logout_usuario(request):
    django_logout(request)
    messages.success(request, "Você saiu do sistema de forma segura.")
    return redirect('home')