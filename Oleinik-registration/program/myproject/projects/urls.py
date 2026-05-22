from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('create/', views.project_create, name='create'),
    path('<str:project_id>/', views.project_detail, name='detail'),  # ← ЭТОТ МАРШРУТ ДОЛЖЕН БЫТЬ!
    path('<str:project_id>/edit/', views.project_edit, name='edit'),
    path('<str:project_id>/duplicate/', views.project_duplicate, name='duplicate'),
    path('<str:project_id>/delete/', views.project_delete, name='delete'),
    path('<str:project_id>/upload/', views.upload_file, name='upload'),
    path('<str:project_id>/download/<str:filename>/', views.download_file, name='download'),
    path('<str:project_id>/export/json/', views.export_project_json, name='export_json'),
    path('save-test/', views.save_project, name='save_test'),
]