from django.shortcuts import render
from datetime import datetime
import pytz


# Create your views here.

def WebSupport(request):
    return render(request,"home.html")

def report(request):
    
    thailand_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(thailand_tz).strftime("%H:%M:%S")
    return render(request, "report.html", {"current_time": current_time})




