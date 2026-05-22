from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    
    # ИСПРАВЛЕНО: убрали full_name, используем отдельные поля
    list_display = ('username', 'email', 'last_name', 'first_name', 'role', 'is_active')
    
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'last_name', 'first_name', 'middle_name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': (
            'last_name', 'first_name', 'middle_name', 'email', 'phone'
        )}),
        ('Профессиональная информация', {'fields': (
            'organization', 'position', 'role'
        )}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'created_at', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'last_name', 'first_name', 'middle_name',
                'phone', 'organization', 'position', 'role'
            ),
        }),
    )
    
    readonly_fields = ('created_at',)
    ordering = ('last_name', 'first_name')