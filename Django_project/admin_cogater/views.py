from django.shortcuts import render


def approve(request):

    reports = Report.objects.filter(status="approved").order_by("-approved_at")

    return render(request, "approve.html", {
        "reports": reports
    })


def reject(request):

    reports = Report.objects.filter(status="rejected").order_by("-created_at")

    return render(request, "reject.html", {
        "reports": reports
    })

def read(request):

    reports = Report.objects.filter(status="read").order_by("-read_at")

    return render(request, "read.html", {
        "reports": reports
    })

def new(request):
    notifications = Report.objects.filter(status="sent").order_by('-created_at')

    context = {
        "notifications": notifications
    }

    return render(request, "new_com.html", context)

def home(request):
    return render(request, "admin_home.html")

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
from django.utils import timezone



def report_detail(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if report.status == "sent":
        report.status = "read"
        report.read_at = timezone.now()
        report.save()

    products = Product.objects.filter(report=report)

    return render(request, "report_detail.html", {
        "report": report,
        "products": products
    })
    
def approve_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if report.status in ["approved", "rejected"]:
        return redirect("report_detail", report_id=report.id)

    report.status = "approved"
    report.approved_at = timezone.now()
    report.approved_by = request.user
    report.save()

    return redirect("report_detail", report_id=report.id)


def reject_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if report.status in ["approved", "rejected"]:
        return redirect("report_detail", report_id=report.id)

    report.status = "rejected"
    report.save()

    return redirect("report_detail", report_id=report.id)