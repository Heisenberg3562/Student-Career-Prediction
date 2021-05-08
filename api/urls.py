from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('predict/', views.predict, name='predict'),
]