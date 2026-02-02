from django.urls import path
from WebSupport import views

urlpatterns = [
    path('', views.WebSupport, name='home'),
    path('info_comp', views.info_comp, name='info_comp'),
    path('info_prod/<str:name>/',views.info_prod, name='info_prod'),
    path('login_com/', views.login_com, name='login_com')
]