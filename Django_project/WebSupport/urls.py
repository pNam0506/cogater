from django.urls import path
from WebSupport import views

urlpatterns = [
    path('home/<str:username_com>/', views.WebSupport, name='home'),
    # path('info_comp', views.info_comp, name='info_comp'),
    path('info_prod/<str:name>/',views.info_prod, name='info_prod'),
    path('login_com/', views.login_com, name='login_com'),
    path('signup_com/', views.signup_com, name='signup_com'),
    path('home/<str:username_com>/info_comp', views.info_comp, name='info_comp')
]