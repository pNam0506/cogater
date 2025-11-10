from django.urls import path
from myapp import views

urlpatterns = [
    path('index',views.index),
    path('about',views.about),
    path('form',views.form),
    path('edit/<person_id>',views.edit),
    path('delete/<person_id>',views.delete),
    path('home/<str:username>/',views.loading, name='user_profile'),
    path('login', views.loginView, name="login"),
    path('signup', views.authView, name='signup')
]
