# myproject/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from myproject.mongodb import projects_collection

def home_view(request):
    return render(request, 'home.html')
