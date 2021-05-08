from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def apiOverview(request):
    return JsonResponse('API Base Point',safe=False)
