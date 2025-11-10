from django.shortcuts import render,redirect
#ส่งข้อความตอบกลับไปยังหน้าเว็บ
from django.http import HttpResponse
from .models import Person, User
from django.contrib import messages
from time import sleep
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password  # ใช้เข้ารหัสรหัสผ่าน


# Create your views here.
def index(request):
    all_person = Person.objects.filter(name = "น้ำ")
    return render(request,"index.html",{"all_person":all_person})

def about(request):
    return render(request,"about.html")

def form(request):
    if request.method == "POST":
        #รับข้อมูล
        name = request.POST["name"]
        age = request.POST["age"]
        
       
        #บันทึกข้อมูล
        person = Person.objects.create(
            name = name,
            age  = age
        )
        person.save()
        messages.success(request,"บันทึกข้อมูลเรียบร้อย")
        #เปลี่ยนเส้นทาง
        return redirect("/")


    else:

        return render(request,"form.html")

def edit(request,person_id):
    if request.method == "POST":
         person = Person.objects.get(id=person_id)
         person.name = request.POST["name"]
         person.age = request.POST["age"]
         person.save()
         messages.success(request,"อัพเดตข้อมูลเรียบร้อย")
         return redirect("/")

    else:
    #ดึงข้อมูลประชากรที่ต้องการเเก้ไข
        person = Person.objects.get(id=person_id)
        return render(request,"edit.html",{"person":person})

def delete(request,person_id):
    person = Person.objects.get(id=person_id)
    person.delete()
    messages.success(request,"ลบข้อมูลเรียบร้อย")
    return redirect("/")

def loading(request, username):
    if request.user.is_authenticated:  # ตรวจว่ามีการล็อกอินอยู่ไหม
        username = request.user.username
        email = request.user.email
        # image = request.user.image.url if request.user.image else None
        return render(request, "loading_page.html", {
            "username": username,
            "email": email,
            # "image": image
        })
    else:
        return redirect("login")

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ตรวจสอบชื่อผู้ใช้และรหัสผ่าน
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ล็อกอินสำเร็จ
            login(request, user)
            messages.success(request, f"ยินดีต้อนรับกลับนะ {username} 💕")
            return redirect("user_profile", username=user.username) # เปลี่ยน 'home' เป็นหน้าที่ต้องการหลังล็อกอิน
        else:
            # ล็อกอินไม่สำเร็จ
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้องนะคั้บ 😿")
            return redirect("login")

    return render(request, "login.html")



def authView(request):
    if request.method == "POST":
        # รับข้อมูลจากฟอร์ม
        username = request.POST.get("username")
        email = request.POST.get("email")
        image = request.FILES.get("image")
        password = request.POST.get("password")

        # ตรวจว่าชื่อผู้ใช้ซ้ำไหม
        if User.objects.filter(username=username).exists():
            messages.error(request, "มีชื่อผู้ใช้นี้อยู่แล้วคั้บ ลองเปลี่ยนชื่อดูน้า")
            return redirect("signup")

        # เข้ารหัสรหัสผ่านก่อนบันทึก
        hashed_password = make_password(password)

        # บันทึกข้อมูล
        user = User.objects.create(
            username=username,
            email=email,
            image=image,
            password=hashed_password
        )

        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้วคั้บ 🎉")
        return redirect("user_profile", username=user.username)  # ไปหน้าโปรไฟล์หลังสมัคร

    return render(request, "signup.html")