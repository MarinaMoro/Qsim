from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from myproject.mongodb import projects_collection
from datetime import datetime
import os
import json
from bson.objectid import ObjectId
from django.conf import settings
import mimetypes
import shutil

@login_required
def project_list(request):
    """Список проектов пользователя"""
    projects = list(projects_collection.find({"user_id": request.user.id}).sort("created_at", -1))
    
    for project in projects:
        project['id'] = str(project['_id'])
        if 'created_at' not in project:
            project['created_at'] = datetime.now()
    
    return render(request, 'projects/list.html', {'projects': projects})

@login_required
def project_create(request):
    """Создание нового проекта с поддержкой загрузки файлов"""
    if request.method == 'POST':
        # Получаем JSON данные из формы, если они есть
        json_data = {}
        try:
            if request.POST.get('json_data'):
                json_data = json.loads(request.POST.get('json_data'))
        except:
            pass
        
        # Создаем проект в MongoDB
        data = {
            "user_id": request.user.id,
            "name": request.POST.get('name', 'Без названия'),
            "description": request.POST.get('description', ''),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "config": json_data,
            "results": {},
            "files": []
        }
        
        result = projects_collection.insert_one(data)
        project_id = str(result.inserted_id)
        
        # Обрабатываем загруженные файлы
        files = request.FILES.getlist('files')
        
        if files:
            # Создаем папку для файлов проекта
            project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', project_id)
            os.makedirs(project_folder, exist_ok=True)
            
            file_infos = []
            for uploaded_file in files:
                # Сохраняем файл
                file_path = os.path.join(project_folder, uploaded_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Информация о файле
                file_info = {
                    "filename": uploaded_file.name,
                    "path": f"{settings.MEDIA_URL}projects/{project_id}/{uploaded_file.name}",
                    "size": uploaded_file.size,
                    "type": uploaded_file.content_type,
                    "uploaded_at": datetime.now()
                }
                file_infos.append(file_info)
            
            # Обновляем проект в MongoDB с информацией о файлах
            projects_collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$push": {"files": {"$each": file_infos}}}
            )
        
        return redirect('projects:list')
    
    return render(request, 'projects/create.html')

@login_required
def project_detail(request, project_id):
    """Детальный просмотр проекта"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project and project['user_id'] == request.user.id:
            project['id'] = str(project['_id'])
            return render(request, 'projects/detail.html', {'project': project})
    except:
        pass
    return redirect('projects:list')

@login_required
def project_edit(request, project_id):
    """Редактирование проекта"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if not project or project['user_id'] != request.user.id:
            return redirect('projects:list')
        
        if request.method == 'POST':
            # Обновляем данные
            update_data = {
                "name": request.POST.get('name', project.get('name')),
                "description": request.POST.get('description', project.get('description')),
                "updated_at": datetime.now()
            }
            
            # Обновляем JSON конфигурацию, если передана
            if request.POST.get('json_data'):
                try:
                    update_data["config"] = json.loads(request.POST.get('json_data'))
                except:
                    pass
            
            projects_collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": update_data}
            )
            
            return redirect('projects:detail', project_id=project_id)
        
        project['id'] = str(project['_id'])
        return render(request, 'projects/edit.html', {'project': project})
    except:
        return redirect('projects:list')

@login_required
def project_duplicate(request, project_id):
    """Дублирование проекта"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project and project['user_id'] == request.user.id:
            # Создаем копию
            new_project = project.copy()
            new_project['_id'] = ObjectId()
            new_project['name'] = f"{project['name']} (копия)"
            new_project['created_at'] = datetime.now()
            new_project['updated_at'] = datetime.now()
            del new_project['_id']
            
            projects_collection.insert_one(new_project)
    except:
        pass
    
    return redirect('projects:list')

@login_required
def project_delete(request, project_id):
    """Удаление проекта"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project and project['user_id'] == request.user.id:
            # Удаляем файлы проекта
            project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(project_id))
            if os.path.exists(project_folder):
                shutil.rmtree(project_folder)
            
            # Удаляем из MongoDB
            projects_collection.delete_one({"_id": ObjectId(project_id)})
    except:
        pass
    
    return redirect('projects:list')

@login_required
def upload_file(request, project_id):
    """Загрузка файла в проект"""
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            
            # Создаем папку для файлов проекта
            project_folder = os.path.join(settings.MEDIA_ROOT, 'projects', str(project_id))
            os.makedirs(project_folder, exist_ok=True)
            
            # Сохраняем файл
            file_path = os.path.join(project_folder, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Информация о файле для MongoDB
            file_info = {
                "filename": uploaded_file.name,
                "path": f"{settings.MEDIA_URL}projects/{project_id}/{uploaded_file.name}",
                "size": uploaded_file.size,
                "type": uploaded_file.content_type,
                "uploaded_at": datetime.now()
            }
            
            # Сохраняем в MongoDB
            projects_collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$push": {"files": file_info}}
            )
            
            return JsonResponse({"success": True, "file": file_info})
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    return JsonResponse({"success": False, "error": "Метод не поддерживается"}, status=400)

@login_required
def download_file(request, project_id, filename):
    """Скачивание файла"""
    file_path = os.path.join(settings.MEDIA_ROOT, 'projects', str(project_id), filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    
    return HttpResponse("Файл не найден", status=404)

@login_required
def export_project_json(request, project_id):
    """Экспорт проекта в JSON"""
    try:
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project and project['user_id'] == request.user.id:
            export_data = {
                "name": project.get('name'),
                "description": project.get('description'),
                "created_at": project.get('created_at').isoformat() if project.get('created_at') else None,
                "updated_at": project.get('updated_at').isoformat() if project.get('updated_at') else None,
                "config": project.get('config', {}),
                "results": project.get('results', {}),
                "files": project.get('files', [])
            }
            
            response = HttpResponse(
                json.dumps(export_data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="project_{project_id}.json"'
            return response
    except Exception as e:
        return HttpResponse(f"Ошибка экспорта: {str(e)}", status=500)
    
    return HttpResponse("Проект не найден", status=404)

@login_required
def save_project(request):
    """Сохранение тестового проекта"""
    data = {
        "user_id": request.user.id,
        "name": "Test project",
        "description": "Это тестовый проект",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "config": {"param": 123, "algorithm": "quantum"},
        "results": {"status": "completed"},
        "files": []
    }
    result = projects_collection.insert_one(data)
    return JsonResponse({
        "status": "saved", 
        "id": str(result.inserted_id),
        "message": "Тестовый проект создан"
    })