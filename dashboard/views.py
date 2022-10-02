from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Log, RegisteredUser
from .models import Holiday
from datetime import datetime
from pytz import timezone
import calendar
import json

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
def generate_report(req, month=None):

    if month is not None and (month.isnumeric() and 12>=int(month)>=1):

        # Get month name and number of holidays
        month_name = calendar.month_name[int(month)]
        holidays = Holiday.objects.get(month_name=month_name).holidays

        # Get number of days of given month
        currentDate = datetime.now(timezone('Asia/Dhaka')).today()
        daysInMonth= calendar.monthrange(currentDate.year, int(month))[1]


        user_logs = []

        registered_users = RegisteredUser.objects.all().order_by('-id')
        for registered_user in registered_users:
            days_present = Log.objects.all().filter(user=registered_user, time_in__month=month).count()
            late_entry = Log.objects.all().filter(user=registered_user, late_join=True).count()
            
            user_logs.append({
                'name': registered_user.name,
                'dept': registered_user.department,
                'holidays': holidays,
                'present': days_present,
                'days_month': daysInMonth,
                'late_entries': late_entry
            })

    else:
        user_logs = False
        month_name = None

    return render(req, 'dashboard/generated_records.html', {'logs': json.dumps(user_logs), 'month_name': month_name})
