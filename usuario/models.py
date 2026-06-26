from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from datetime import date
import re

def validar_maioridade(data_nascimento):
    if data_nascimento:
        hoje = date.today()
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
        if idade < 18:
            raise ValidationError("Você precisa ter mais de 18 anos para se cadastrar.")

def validar_cpf(value):

    cpf = re.sub(r'[^0-9]', '', value)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("CPF inválido.")

class GerenciarUsuario(BaseUserManager):

    def create_user(self, nome, nomeUsuario, email, telefone, endereco, password=None, **extra_fields):
        if not email:
            raise ValueError('Usuário deve ter um endereço de email.')
        
        if not nome:
            raise ValueError('Nome do usuário é obrigatório.')
        
        usuario = self.model(
            email=email,
            nomeUsuario=nomeUsuario,
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            **extra_fields
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, nome, nomeUsuario, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            nome=nome,
            nomeUsuario=nomeUsuario,
            email=email,
            telefone="00000000000",        # Valor padrão apenas para o Admin
            endereco="Sistema Central",    # Valor padrão apenas para o Admin
            password=password,
            **extra_fields
        )

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=80)
    nomeUsuario = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=250)
    data_nascimento = models.DateField(validators=[validar_maioridade], blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf], blank=True, null=True)
    renda_mensal_casa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moradores_casa = models.PositiveIntegerField(default=1)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'nomeUsuario']

    objects = GerenciarUsuario()

    def __str__(self):
        return self.nomeUsuario
    
    @property
    def renda_per_capita(self):
        if self.moradores_casa and self.moradores_casa > 0:
            return self.renda_mensal_casa / self.moradores_casa
        
        return self.renda_mensal_casa