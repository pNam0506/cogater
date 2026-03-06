from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard.html")

from .models import Notification

def admin_dashboard(request):

    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')

    context = {
        "notifications": notifications
    }

    return render(request,"admin_dashboard.html",context)

from django.shortcuts import render, get_object_or_404, redirect
from WebSupport.models import *



def report_detail(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    # เมื่อ admin เปิด report → เปลี่ยน status เป็น read
    if report.status == "sent":
        report.status = "read"
        report.save()

    products = Product.objects.filter(report=report)

    return render(request, "report_detail.html", {
        "report": report,
        "products": products
    })
    
def approve_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    report.status = "approved"
    report.save()

    return redirect("admin_dashboard")

def reject_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    report.status = "rejected"
    report.save()

    return redirect("admin_dashboard")