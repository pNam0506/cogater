from django.shortcuts import render,redirect
#ส่งข้อความตอบกลับไปยังหน้าเว็บ
from django.http import HttpResponse
from myapp.models import Person, User
from django.contrib import messages
from time import sleep
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    user = get_object_or_404(User, username=username)
    return render(request, "loading_page.html", {"user_profile": user})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"ยินดีต้อนรับ {username}!")
                return redirect("user_profile", username=user.username)  # เปลี่ยน 'home' เป็นชื่อหน้าเว็บที่ต้องการไปหลังล็อกอิน
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        else:
            messages.error(request, "กรุณากรอกข้อมูลให้ถูกต้อง")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def authView(request):
    # if request.method == "POST":
    #     form = UserCreationForm(request.POST or None)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     form = UserCreationForm()
    # return render(request, "signup.html", {"form": form})
    if request.method == "POST":
        #รับข้อมูล
        username = request.POST["username"]
        email = request.POST["email"]
        image = request.FILES.get("image")
        password = request.POST["password"]
       
        #บันทึกข้อมูล
        user = User.objects.create(
            username = username,
            email  = email,
            image = image,
            password = password


        )
        user.save()
        messages.success(request,"บันทึกข้อมูลเรียบร้อย")
        #เปลี่ยนเส้นทาง
        return redirect("user_profile", username=user.username)  # เปลี่ยน 'home' เป็นชื่อหน้าเว็บที่ต้องการไปหลังล็อกอิน


    else:

        return render(request,"signup.html")
