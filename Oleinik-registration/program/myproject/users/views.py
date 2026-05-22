from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm

def register_view(request):
    """Представление для регистрации нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'users/register.html', context)

def login_view(request):
    """Представление для входа пользователя"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'users/login.html', context)

def logout_view(request):
    """Представление для выхода пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')

@login_required
def profile_view(request):
    """Представление для просмотра профиля пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def account_settings(request):
    """Страница настроек аккаунта"""
    # Получаем список подключенных социальных аккаунтов
    connected_socials = []
    try:
        from social_django.models import UserSocialAuth
        connected_socials = [sa.provider for sa in UserSocialAuth.objects.filter(user=request.user)]
    except:
        pass
    
    return render(request, 'users/settings.html', {
        'connected_socials': connected_socials
    })

@login_required
def update_profile(request):
    """Обновление профиля"""
    if request.method == 'POST':
        user = request.user
        user.last_name = request.POST.get('last_name', '')
        user.first_name = request.POST.get('first_name', '')
        user.middle_name = request.POST.get('middle_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.organization = request.POST.get('organization', '')
        user.position = request.POST.get('position', '')
        user.role = request.POST.get('role', 'student')
        
        # Обработка фото
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Профиль успешно обновлен!')
    
    return redirect('users:account_settings')

@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('users:account_settings')

@login_required
def connect_social(request, provider):
    """Подключение социального аккаунта"""
    return redirect(f'/oauth/login/{provider}/?next={request.path}')

@login_required
def disconnect_social(request, provider):
    """Отключение социального аккаунта"""
    try:
        from social_django.models import UserSocialAuth
        social = UserSocialAuth.objects.get(user=request.user, provider=provider)
        social.delete()
        messages.success(request, f'Аккаунт {provider} отключен')
    except:
        messages.error(request, 'Ошибка при отключении')
    
    return redirect('users:account_settings')