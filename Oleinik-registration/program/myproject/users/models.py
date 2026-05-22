from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Базовые поля (переопределяем)
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
        help_text="Обязательное поле. Не более 150 символов."
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name="E-mail",
        help_text="Обязательное поле."
    )
    
    # 1. Фамилия (обязательная)
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
        help_text="Обязательное поле."
    )
    
    # 2. Имя (обязательная)
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        help_text="Обязательное поле."
    )
    
    # 3. Отчество (не обязательно)
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Отчество",
        help_text="Необязательное поле."
    )
    
    # 5. Телефон (не обязательно)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+79991234567'. Допускается до 15 цифр."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Необязательное поле."
    )
    
    # 6. Место работы/учебы (не обязательно)
    organization = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место работы/учёбы",
        help_text="Необязательное поле."
    )
    
    # 7. Должность (не обязательно)
    position = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Должность",
        help_text="Необязательное поле."
    )
    
    # Роли
    ROLE_CHOICES = [
        ("school", "Школьник"),
        ("student", "Студент"),
        ("teacher", "Преподаватель"),
        ("employee", "Сотрудник профильного предприятия"),
        ("admin", "Администратор"),
    ]
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default="student",
        verbose_name="Роль"
    )
    
    # Дополнительные поля
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата регистрации"
    )
    
 # Фото профиля
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Фото профиля"
    )
    
    # Статус аккаунта
    email_confirmed = models.BooleanField(
        default=False, 
        verbose_name="Email подтвержден"
    )
    
    account_status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Активен"),
            ("inactive", "Неактивен"),
            ("blocked", "Заблокирован"),
        ],
        default="active",
        verbose_name="Статус аккаунта"
    )

    # Настройки приватности
    projects_public_by_default = models.BooleanField(
        default=False,
        verbose_name="Новые проекты публичны по умолчанию"
    )
    
    # Уведомления
    email_notifications = models.BooleanField(
        default=True, 
        verbose_name="Email уведомления"
    )
    
    # Последняя активность (обновляется автоматически)
    last_activity = models.DateTimeField(
        auto_now=True, 
        verbose_name="Последняя активность"
    )

    # Вычисляемое поле ФИО (НЕ хранится в БД)
    @property
    def full_name(self):
        """Полное ФИО (вычисляемое свойство)"""
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)
    
    def get_full_name_display(self):
        """Для отображения в шаблонах"""
        return self.full_name
    
    def get_role_display(self):
        """Отображение роли на русском"""
        role_dict = dict(self.ROLE_CHOICES)
        return role_dict.get(self.role, "Не указана")
    
    def get_short_name(self):
        """Короткое имя (Имя Отчество)"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name}"
        return self.first_name
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    @property
    def avatar_url(self):
        """URL аватара или заглушка"""
        if self.avatar:
            return self.avatar.url
        return None
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['last_name', 'first_name']

