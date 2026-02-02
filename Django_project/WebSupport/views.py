from django.shortcuts import render, redirect
from datetime import datetime
import pytz
from .models import Company, Product
from django.contrib import messages


# Create your views here.

def WebSupport(request):
    return render(request,"home.html")

def info_comp(request):
    
    thailand_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(thailand_tz).strftime("%H:%M:%S")
    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        name = request.POST.get("name")
        store = request.POST.get("store")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        operator = request.POST.get("operator")
        website = request.POST.get("website")
        logo = request.FILES.get("picture_multi")
        

        # ตรวจว่าชื่อผู้ใช้ซ้ำไหม
        if Company.objects.filter(name=name).exists():
            messages.error(request, "มีชื่อผู้ใช้นี้อยู่แล้วคั้บ ลองเปลี่ยนชื่อดูน้า")
            return redirect("info_comp")

        # # เข้ารหัสรหัสผ่านก่อนบันทึก
        # hashed_password = make_password(password)

        # บันทึกข้อมูล
        user = Company.objects.create(
             name=name,
            store=store,
            address=address,
            email=email,
            phone=phone,
            operator=operator,
            website=website,
            logo=logo
            
        )

        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้วคั้บ 🎉")
        return redirect("info_prod", name=user.name)
        
    return render(request, "info_comp.html", {"current_time": current_time})
    
def info_prod(request, name):
    company = Company.objects.filter(name=name).first()

    if not company:
        messages.error(request, "ไม่พบบริษัทนี้")
        return redirect("info_comp")

    products = Product.objects.filter(company=company)

    return render(request, "info_prod.html", {
        "company": company,
        "products": products
    })
    
def login_com(request):
    
    return render(request,"info_comp.html")
    





    

# def save_company(request):
#     if request.method == "POST":
#         company_name = request.POST.get("company_name")

#         company = Company.objects.create(name=company_name)

#         # จำชื่อบริษัทไว้ใช้ต่อ
#         request.session["company_id"] = company.id

#         return redirect("info_page")


