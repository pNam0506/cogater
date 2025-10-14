from django.urls import path
from WebSupport import views

urlpatterns = [
    path('', views.WebSupport, name='home'),
]