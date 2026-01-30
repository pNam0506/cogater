from django.shortcuts import render, redirect
from datetime import datetime
import pytz
from .models import Company, Product


# Create your views here.

def WebSupport(request):
    return render(request,"home.html")

def report(request):
    
    thailand_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(thailand_tz).strftime("%H:%M:%S")
    return render(request, "report.html", {"current_time": current_time})


# def save_company(request):
#     if request.method == "POST":
#         company_name = request.POST.get("company_name")

#         company = Company.objects.create(name=company_name)

#         # จำชื่อบริษัทไว้ใช้ต่อ
#         request.session["company_id"] = company.id

#         return redirect("info_page")


