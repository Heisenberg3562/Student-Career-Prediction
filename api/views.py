from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Predict': '/predict/',
    }
    return Response(api_urls)


@api_view(['GET'])
def predict(request):
    id = request['id']
    return JsonResponse(id, safe=False)
