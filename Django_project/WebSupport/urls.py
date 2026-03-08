from django.urls import path
from WebSupport import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/<str:username_com>/', views.WebSupport, name='home'),
    # path('info_comp', views.info_comp, name='info_comp'),
    path("info_prod/<int:company_id>/", views.info_prod, name="info_prod"),    
    path('login_com/', views.login_com, name='login_com'),
    path('signup_com/', views.signup_com, name='signup_com'),
    path('home/<str:username_com>/info_comp', views.info_comp, name='info_comp'),
    path(
        "product/edit/<int:product_id>/",
        views.edit_product,
        name="edit_product"
    ),

path(
    'get_documents/<int:report_id>/',
    views.get_documents,
    name='get_documents'
),
path('report/edit/<int:report_id>/', views.edit_report, name='edit_report'),
path("comment/<int:report_id>/", views.reject_reason, name="comment"),
path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    
]