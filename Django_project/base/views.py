from django.shortcuts import render

# Create your views here.
def intro(request):
    return render(request, 'intro.html')

# def login(request):
#     return render(request, 'login.html')