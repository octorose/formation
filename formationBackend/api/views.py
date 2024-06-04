from django.shortcuts import render
from django.http import JsonResponse
from .models import Personnel

def personnel_list(request):
    Personnel = Personnel.objects.all()
    data = {'personnel': list(Personnel.values())}
    return JsonResponse(data)