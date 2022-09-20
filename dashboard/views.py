from django.shortcuts import render
from datetime import datetime, timedelta, date
from pytz import timezone
from django.contrib.auth.decorators import login_required
from main.models import Log


@login_required(login_url='login')
def dashboard_today(req):
    today_date = datetime.now(timezone('Asia/Dhaka')).today()
    user_logs = Log.objects.all().filter(time_in__date=today_date).order_by('-id')
    return render(req, 'dashboard/records.html', {'logs': user_logs, 'heading': "Today's Record"})


@login_required(login_url='login')
def dashboard_master(req):
    user_logs = Log.objects.all().order_by('-id')
    return render(req, 'dashboard/records.html', {'logs': user_logs, 'heading': "Master Record"})


@login_required(login_url='login')
def dashboard(req):
    return render(req, 'dashboard/dashboard.html')


@login_required(login_url='login')
def generate_report(req, days=None):

    if days is not None:
        enddate = datetime.now().today().replace(tzinfo=timezone('Asia/Dhaka'))
        startdate = (enddate - timedelta(days=days))
        user_logs = Log.objects.all().filter(time_in__range=[startdate, enddate]).order_by('-id')
    else:
        user_logs = False

    return render(req, 'dashboard/generated_records.html', {'logs': user_logs})
