from django.db import models
from django.conf import settings
import uuid
import os

class Project(models.Model):
    """Модель проекта в Django (для связи с пользователями)"""
    
    PROJECT_TYPES = [
        ('quantum', 'Квантовый алгоритм'),
        ('simulation', 'Симуляция'),
        ('circuit', 'Квантовая схема'),
        ('other', 'Другое'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    
    # Основная информация (дублируется в MongoDB)
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='quantum')
    
    # Ссылка на документ
    mongodb_id = models.CharField(max_length=50, blank=True, help_text="ID документа в MongoDB")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    def __str__(self):
        return self.title
    
    def get_mongodb_data(self):
        """Получает данные проекта из MongoDB"""
        from myproject.mongodb import projects_collection
        if self.mongodb_id:
            try:
                from bson.objectid import ObjectId
                return projects_collection.find_one({'_id': ObjectId(self.mongodb_id)})
            except:
                return None
        return None

class ProjectFile(models.Model):
    """Модель для файлов проекта (хранятся на диске)"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='projects/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.filename
    
    def save(self, *args, **kwargs):
        if self.file:
            self.filename = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)