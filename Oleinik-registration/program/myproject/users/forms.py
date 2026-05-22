from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.validators import RegexValidator
from captcha.fields import CaptchaField
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Обязательные поля
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'})
    )
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'})
    )
    
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        label="Отчество",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (при наличии)'})
    )
    
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )
    
    # Необязательные поля
    phone = forms.CharField(
        max_length=17,
        required=False,
        label="Телефон",
        help_text="Формат: +79991234567",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79991234567'})
    )
    
    organization = forms.CharField(
        max_length=255,
        required=False,
        label="Место работы/учёбы",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: МГУ, Яндекс и т.д.'})
    )
    
    position = forms.CharField(
        max_length=150,
        required=False,
        label="Должность",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: студент, разработчик и т.д.'})
    )
    
    # Роль
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='student',
        required=True,
        label="Роль",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Пароли
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        help_text="Пароль должен содержать минимум 8 символов."
    )
    
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        help_text="Для подтверждения введите пароль ещё раз."
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'last_name', 
            'first_name', 
            'middle_name',
            'email',
            'phone',
            'organization',
            'position',
            'role',
            'password1', 
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Придумайте логин'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].help_text = "Необязательное поле. Если не указать, будет создан из email."
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Автозаполнение username
        if not user.username:
            user.username = user.email.split('@')[0]
        
        # Уникальность username
        original_username = user.username
        counter = 1
        while CustomUser.objects.filter(username=user.username).exists():
            user.username = f"{original_username}{counter}"
            counter += 1
        
        # ВАЖНО: устанавливаем бэкенд
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        if commit:
            user.save()
        
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа с капчей"""
    
    captcha = CaptchaField(
        label='Введите код с картинки',
        help_text='Для защиты от автоматического входа',
        error_messages={
            'invalid': 'Неправильный код с картинки',
            'required': 'Пожалуйста, введите код с картинки'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"

# ============================================
# НОВАЯ ФОРМА ДЛЯ РЕДАКТИРОВАНИЯ ПРОФИЛЯ
# ============================================

class ProfileEditForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    # Переопределяем поля для добавления атрибутов CSS
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        label="Отчество",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    phone = forms.CharField(
        max_length=17,
        required=False,
        label="Телефон",
        help_text="Формат: +79991234567",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79991234567'})
    )
    
    organization = forms.CharField(
        max_length=255,
        required=False,
        label="Место работы/учёбы",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    position = forms.CharField(
        max_length=150,
        required=False,
        label="Должность",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        required=True,
        label="Роль",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    avatar = forms.ImageField(
        required=False,
        label="Фото профиля",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'last_name', 'first_name', 'middle_name',
            'email', 'phone', 'avatar',
            'organization', 'position', 'role'
        ]
    
    def clean_email(self):
        """Проверка уникальности email (исключая текущего пользователя)"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Этот email уже используется другим пользователем.")
        return email
    
    def clean_phone(self):
        """Очистка и валидация телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Убираем все нецифровые символы, кроме +
            import re
            phone = re.sub(r'[^\d+]', '', phone)
            if not re.match(r'^\+?\d{10,15}$', phone):
                raise forms.ValidationError("Некорректный формат телефона.")
        return phone