from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.account_settings, name='account_settings'),  # ← ЭТА СТРОКА НУЖНА!
    path('settings/update/', views.update_profile, name='update_profile'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/connect/<str:provider>/', views.connect_social, name='connect_social'),
    path('settings/disconnect/<str:provider>/', views.disconnect_social, name='disconnect_social'),
]