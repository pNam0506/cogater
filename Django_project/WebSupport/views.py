from django.shortcuts import render, redirect

import pytz
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password  
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from admin_cogater.models import Notification



# Create your views here.

# def WebSupport(request, username_com):

#     company = get_object_or_404(
#         Company.objects.select_related("company_id"),
#         company_id__username_com=username_com
#     )

#     # Get first report of this company
#     report = Report.objects.filter(company=company).first()

#     # Get all products of this company (through report)
#     products = Product.objects.filter(
#         report__company=company
#     ).select_related("report").prefetch_related("sizes")
    
#     documents = CollabDocument.objects.filter(report__company=company)

#     return render(request, "home.html", {
#         "company": company,
#         "report": report,
#         "products": products
#     })

def WebSupport(request, username_com):

    company = get_object_or_404(
        Company.objects.select_related("company_id"),
        company_id__username_com=username_com
    )

    reports = Report.objects.filter(company=company).prefetch_related(
    "products__sizes",
    "documents"
)

    return render(request, "home.html", {
        "company": company,
        "reports": reports
    })

def info_comp(request, username_com):

    users = get_object_or_404(sign_com, username_com=username_com)

    # 🔎 เช็คว่า account นี้มี company แล้วไหม
    existing_company = Company.objects.filter(company_id=users).first()

    if existing_company:
        # ✅ ถ้ามี → ไป info_prod เลย
        return redirect("info_prod", company_id=existing_company.id)

    # ❌ ยังไม่มี → แสดงฟอร์มสร้าง
    if request.method == "POST":

        name = request.POST.get("name")
        store = request.POST.get("store")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        operator = request.POST.get("operator")
        website = request.POST.get("website")
        logo = request.FILES.get("picture_multi")

        company = Company.objects.create(
            company_id=users,
            name=name,
            store=store,
            address=address,
            email=email,
            phone=phone,
            operator=operator,
            website=website,
            logo=logo
        )

        return redirect("info_prod", company_id=company.id)

    return render(request, "info_comp.html", {
        "users": users
    })


# ===============================
# SHOW PRODUCTS OF A REPORT
# ===============================

def info_prod(request, company_id):

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":

        # ===============================
        # 1️⃣ VALIDATE DATE
        # ===============================
        start_date_raw = request.POST.get("start_date")
        end_date_raw = request.POST.get("end_date")

        if not start_date_raw or not end_date_raw:
            messages.error(request, "Start date and End date are required.")
            return redirect("info_prod", company_id=company.id)

        try:
            start_date = datetime.strptime(start_date_raw, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_raw, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect("info_prod", company_id=company.id)

        if end_date < start_date:
            messages.error(request, "End date cannot be before Start date.")
            return redirect("info_prod", company_id=company.id)

        # ===============================
        # 2️⃣ VALIDATE COLLAB TYPE
        # ===============================
        collab_type = request.POST.get("collab_type")
        other_collab = request.POST.get("collab_type_other")

        if not collab_type:
            messages.error(request, "Collab type is required.")
            return redirect("info_prod", company_id=company.id)

        if collab_type != "Other":
            other_collab = None

        ads_image = request.FILES.get("ads_image")
        name = request.POST.get("collection_name")
        desc = request.POST.get("collection_desc")

        # ===============================
        # 3️⃣ SAVE DATA (ATOMIC)
        # ===============================
        try:
            with transaction.atomic():

                # ---------------------------
                # CREATE REPORT
                # ---------------------------
                report = Report.objects.create(
                    company=company,
                    name=name,
                    description = desc,
                    collab_type=collab_type,
                    other_collab=other_collab,
                    start_date=start_date,
                    end_date=end_date,
                    ads_image=ads_image,
                    status="sent"
                )

                # ---------------------------
                # 🔔 CREATE NOTIFICATION
                # ---------------------------
                Notification.objects.create(
                    report=report,
                    message=f"New report from {company.name}"
                )

                # ---------------------------
                # SAVE DOCUMENTS
                # ---------------------------
                documents = request.FILES.getlist("documents")

                for doc in documents:
                    CollabDocument.objects.create(
                        report=report,
                        file=doc
                    )

                # ---------------------------
                # SAVE PRODUCTS
                # ---------------------------
                product_count = int(request.POST.get("product_count", 0))

                for i in range(product_count):

                    image = request.FILES.get(f"product_image_{i}")
                    detail = request.POST.get(f"product_detail_{i}")

                    # ถ้า product ว่างจริง ๆ ข้าม
                    if not image and not detail:
                        continue

                    product = Product.objects.create(
                        report=report,
                        image=image,
                        detail=detail
                    )

                    # ---------------------------
                    # SAVE PRODUCT SIZES
                    # ---------------------------
                    size_count = int(request.POST.get(f"size_count_{i}", 0))

                    for j in range(size_count):

                        size = request.POST.get(f"product_{i}_size_{j}")
                        price = request.POST.get(f"product_{i}_price_{j}")

                        if size and price:
                            ProductSize.objects.create(
                                product=product,
                                size=size,
                                price=price
                            )

        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")
            return redirect("info_prod", company_id=company.id)

        messages.success(request, "Report created successfully.")
        return redirect("info_prod", company_id=company.id)

    return render(request, "info_prod.html", {
        "company": company
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


def edit_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":

        detail = request.POST.get("detail")
        image = request.FILES.get("image")

        product.detail = detail

        if image:
            product.image = image

        product.save()

        return redirect("home", username_com=product.report.company.company_id.username_com)

    return render(request, "edit_product.html", {
        "product": product
    })
    


def get_documents(request, report_id):

    docs = CollabDocument.objects.filter(report_id=report_id)

    data = []

    for d in docs:
        data.append({
            "url": d.file.url,
            "name": d.file.name.split("/")[-1]
        })

    return JsonResponse(data, safe=False)

def edit_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if report.status != "sent":
        messages.error(request, "This report can no longer be edited.")
        return redirect("home", report.company.company_id.username_com)

    if request.method == "POST":

        report.name = request.POST.get("name")
        report.start_date = request.POST.get("start_date")
        report.end_date = request.POST.get("end_date")

        report.save()

        messages.success(request, "Report updated.")
        return redirect("home", report.company.company_id.username_com)

    return render(request, "edit_report.html", {
        "report": report
    })