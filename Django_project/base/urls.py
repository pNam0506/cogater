from django.urls import path
from base import views


urlpatterns = [
    path('', views.intro, name='home'),
    # path('login', views.login, name='login')

]