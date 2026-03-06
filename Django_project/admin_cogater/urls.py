from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path("report/<int:report_id>/", views.report_detail, name="report_detail"),
     path('approve/<int:report_id>/', views.approve_report, name='approve_report'),
         path('reject/<int:report_id>/', views.reject_report, name='reject_report'),
         
]