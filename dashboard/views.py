from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.models import Log, RegisteredUser
from .models import Holiday
from datetime import datetime
from pytz import timezone
import calendar
import json


@login_required(login_url='login')
def dashboard_today(req, page_no=1):
    today_date = datetime.now(timezone('Asia/Dhaka')).today()
    user_logs = Log.objects.filter(
        time_in__date=today_date, approved=True).order_by('-id')

    paginator = Paginator(user_logs, 20)
    data_per_page = paginator.get_page(page_no)
    paginator_list = list(
        paginator.get_elided_page_range(page_no, on_each_side=1))

    return render(req, 'dashboard/records.html', {
        'logs': data_per_page,
        'paginator_list': paginator_list,
        'heading': "Today's Record",
        'master': False
    })


@login_required(login_url='login')
def dashboard_master(req, page_no=1):
    user_logs = Log.objects.all().order_by('-id')

    paginator = Paginator(user_logs, 20)
    data_per_page = paginator.get_page(page_no)
    paginator_list = list(
        paginator.get_elided_page_range(page_no, on_each_side=1)
    )

    return render(req, 'dashboard/records.html', {
        'logs': data_per_page,
        'paginator_list': paginator_list,
        'heading': "Master Record",
        'master': True
    })


@login_required(login_url='login')
def approval_page(req):

    if req.method == 'POST':
        log_ids = req.POST.get('emails')
        log_ids = json.loads(log_ids)
        Log.objects.filter(id__in=log_ids).update(approved=True)
        return HttpResponse(json.dumps({'stat': True}))

    today_date = datetime.now(timezone('Asia/Dhaka')).today()
    user_logs = Log.objects.all().filter(time_in__date=today_date,
                                         approved=False).order_by('-id')

    return render(req, 'dashboard/approval.html', {
        'logs': user_logs
    })


@login_required(login_url='login')
def dashboard(req):
    return render(req, 'dashboard/dashboard.html')


@login_required(login_url='login')
def generate_report(req, month=None):

    if month is not None and (month.isnumeric() and 12 >= int(month) >= 1):

        # Get month name and number of holidays
        month_name = calendar.month_name[int(month)]
        holidays = Holiday.objects.get(month_name=month_name).holidays

        # Get number of days of given month
        currentDate = datetime.now(timezone('Asia/Dhaka')).today()
        daysInMonth = calendar.monthrange(currentDate.year, int(month))[1]

        user_logs = []
        registered_users = RegisteredUser.objects.all().order_by('-id')

        for registered_user in registered_users:

            days_present = Log.objects.filter(
                user=registered_user, time_in__month=month).count()

            late_entry = Log.objects.filter(
                user=registered_user, time_in__month=month,
                late_join=True, approved=True
            ).count()

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
