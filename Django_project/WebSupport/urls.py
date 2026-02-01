from django.urls import path
from WebSupport import views

urlpatterns = [
    path('', views.WebSupport, name='home'),
    path('info_comp', views.info_comp, name='info_comp'),

]