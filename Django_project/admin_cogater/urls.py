from django.urls import path
from . import views

urlpatterns = [
    path('notification', views.admin_dashboard, name='admin_dashboard'),
    path("report/<int:report_id>/", views.report_detail, name="report_detail"),
    path('approve/<int:report_id>/', views.approve_report, name='approve_report'),
    path('reject/<int:report_id>/', views.reject_report, name='reject_report'),
    path('', views.home, name='admin_home'),
    path('read', views.read, name='read'),
    path('reject', views.reject, name='reject'),
    path('approve', views.approve, name='approve'),
    path('new', views.new, name='new'),
    path('check-new-reports/',views.check_new_reports,name='check_new_reports'),
   
]