from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import UsuarioForm

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    form = UsuarioForm
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('biografia', 'data_nascimento')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('biografia', 'data_nascimento')}),
    )
    list_display = (
        'username', 'email', 'is_staff', 'is_active', 'is_superuser'
    )