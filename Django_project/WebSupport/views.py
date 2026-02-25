from django.shortcuts import render, redirect
from datetime import datetime
import pytz
from .models import Company, Product, sign_com
from django.contrib import messages
from django.contrib.auth.hashers import make_password  
from django.contrib.auth.hashers import check_password


# Create your views here.

def WebSupport(request, username_com):

    products = Product.objects.select_related(
        "company", "company__company_id"
    ).filter(
        company__company_id__username_com=username_com
    )

    return render(request, "home.html", {
        "products": products
    })

def info_comp(request, username_com):

    users = sign_com.objects.get(username_com=username_com)

    thailand_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(thailand_tz).strftime("%H:%M:%S")

    if request.method == "POST":

        name = request.POST.get("name")
        store = request.POST.get("store")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        operator = request.POST.get("operator")
        website = request.POST.get("website")
        logo = request.FILES.get("picture_multi")

        if Company.objects.filter(name=name).exists():

            messages.error(request, "มีชื่อผู้ใช้นี้อยู่แล้ว")

            return redirect("info_comp", username_com=username_com)


        Company.objects.create(

            company_id=users,   # ⭐⭐⭐ เพิ่มบรรทัดนี้

            name=name,
            store=store,
            address=address,
            email=email,
            phone=phone,
            operator=operator,
            website=website,
            logo=logo

        )

        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้ว")

        return redirect("info_prod", name=name)


    return render(request, "info_comp.html", {

        "current_time": current_time,
        "users": users

    })
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

    if request.method == "POST":

        username_com = request.POST.get("username_com")
        password_com = request.POST.get("password_com")

        user = sign_com.objects.filter(username_com=username_com).first()

        if user and check_password(password_com, user.password_com):

            return redirect("home", username_com=username_com)

        else:

            messages.error(
                request,
                "Invalid username or password"
            )

            return redirect("login_com")

    return render(request, "login_com.html")
def signup_com(request):
    
    if request.method == "POST":
        username_com = request.POST.get("username_com")
        email_com = request.POST.get("email_com")
        password_com = request.POST.get("password_com")
        image_com = request.FILES.get("image_com")
    
        if sign_com.objects.filter(username_com=username_com).exists():
            messages.error(request, "มีชื่อผู้ใช้นี้อยู่แล้วคั้บ ลองเปลี่ยนชื่อดูน้า")
            return redirect("login_com")

        # # เข้ารหัสรหัสผ่านก่อนบันทึก
        # hashed_password = make_password(password)
        hashed_password = make_password(password_com)

        # บันทึกข้อมูล
        user = sign_com.objects.create(
            username_com=username_com,
            email_com=email_com,
            password_com=hashed_password,
            image_com=image_com
            )

        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้วคั้บ 🎉")
        return redirect('info_comp', username_com=username_com)
    
    
    return render(request,"signup_com.html")
    





    

# def save_company(request):
#     if request.method == "POST":
#         company_name = request.POST.get("company_name")

#         company = Company.objects.create(name=company_name)

#         # จำชื่อบริษัทไว้ใช้ต่อ
#         request.session["company_id"] = company.id

#         return redirect("info_page")


