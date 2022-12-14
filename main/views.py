from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from dashboard.models import Info
from PIL import Image
from datetime import datetime
from pytz import timezone
import json

from . import face_recognize
from .functions import hr_to_hm, location_validator



def home(req):
    is_signed_in = req.session.get('is_signed_in', None)
    username = req.session.get('user_name', None)
    email = req.session.get('user_email', None)

    now_date = str(datetime.now(timezone('Asia/Dhaka')).date())

    if now_date != req.session.get('login_date', ''):
        signed_in = False
        req.session['is_signed_in'] = 'N'
    else:
        signed_in = False if is_signed_in == 'N' or is_signed_in is None  else True

    if username is None or email is None:
        msg = '<br><br><br>'
    else:
        msg = f"Username: <b>{username}</b> <br>Email: <b>{email}</b> <br> {'Signed In' if signed_in else 'Signed out'}"

    return render(req, 'home.html', {
        'signed_in': signed_in,
        'msg': msg
    })



def sign_in(req):
    saved_email = req.session.get('user_email', "")

    if req.method == 'POST':

        position = req.POST.get('position')
        email = req.POST.get('email')
        position_url = req.POST.get('position_url')
        coords_lat = req.POST.get('coords_lat')
        coords_lon = req.POST.get('coords_lon')

        user = RegisteredUser.objects.filter(email=email).first()

        if user is None:
            return HttpResponse(json.dumps({'stat': 'not_user'}))

        # Target image
        target_img = Image.open(
            req.FILES.get('img')
        )

        # Reference image
        ref_imgs = user.user_images.all()
        for ref_img in ref_imgs:
            new_ref_img = Image.open(ref_img.image)

            # Comparing images and Logging
            if face_recognize.compare(target_img, new_ref_img):
                
                now_time = datetime.now(timezone('Asia/Dhaka'))
                join_in = Info.objects.get(name='main').time_in
                delta_time = (datetime.combine(now_time.today(), join_in).replace(tzinfo=timezone('Asia/Dhaka')) - now_time).total_seconds()

                # Delay sign in
                delayIn = ((now_time - datetime.combine(now_time.today(), join_in).replace(tzinfo=timezone('Asia/Dhaka'))).total_seconds() / 3600)
                delayIn_hr_min = hr_to_hm(delayIn)
                delay_in = f"{delayIn_hr_min} Late" if delayIn > 0 else f"{delayIn_hr_min} Early"
                
                # Approval of Location
                approved = location_validator(coords_lat, coords_lon)

                # Storing to DB
                user_log = Log(time_in=now_time, name=user.name, user=user, location_in=position, delay_in=delay_in)
                user_log.location_in_url = position_url
                user_log.late_join = True if delta_time < 0 else False
                user_log.approved = approved
                user_log.save()

                # Save into Session
                req.session['is_signed_in'] = 'Y'
                req.session['user_id'] = user_log.id
                req.session['user_name'] = ref_img.user.name
                req.session['user_email'] = ref_img.user.email
                req.session['login_date'] = str(now_time.date())

                return HttpResponse(json.dumps({'stat': 'is_user'}))

        # Couldn't match image
        return HttpResponse(json.dumps({'stat': 'face_unmatched'}))

    if req.session.get('is_signed_in', None) == 'Y':
        return redirect('/')
    
    else:
        return render(req, 'user/sign_in.html', {'email': saved_email})




def sign_out(req):
    is_signed_in = req.session.get('is_signed_in', None)

    if req.method == 'POST' and is_signed_in == 'Y':

        email = req.session.get('user_email', None)
        position = req.POST.get('position')
        position_url = req.POST.get('position_url')

        # Target image
        user = RegisteredUser.objects.filter(email=email).first()
        target_img = Image.open(
            req.FILES.get('img')
        )
        # Reference image
        ref_imgs = user.user_images.all()
        for ref_img in ref_imgs:
            new_ref_img = Image.open(ref_img.image)

            # Comparing images and Logging
            if face_recognize.compare(target_img, new_ref_img):

                # Getting signout time and duration
                log_id = req.session.get('user_id', '')
                signout_time = datetime.now(timezone('Asia/Dhaka'))
                user_log = Log.objects.get(id=log_id)
                delta_time = signout_time - user_log.time_in
                delta_time = round((delta_time.total_seconds() / 3600), 3)

                # Checking late or not
                leave_time = Info.objects.get(name='main').time_out
                if ((datetime.combine(signout_time.today(), leave_time).replace(tzinfo=timezone('Asia/Dhaka')) - signout_time).total_seconds() < 0):
                    user_log.late_leave = True
                else:
                    user_log.late_leave = False

                # Delay sign in
                delayOut = ((signout_time - datetime.combine(signout_time.today(), leave_time).replace(tzinfo=timezone('Asia/Dhaka'))).total_seconds() / 3600)
                delayOut_hr_min = hr_to_hm(delayOut)
                delay_out = f"{delayOut_hr_min} Late" if delayOut > 0 else f"{delayOut_hr_min} Early"
                user_log.delay_out = delay_out

                # Storing user log to DB
                user_log.time_out = signout_time
                user_log.total_hours = hr_to_hm(delta_time)
                user_log.location_out = position
                user_log.location_out_url = position_url
                user_log.save()
                req.session['is_signed_in'] = 'N'

                return HttpResponse(json.dumps({'stat': 'is_user'}))


        # Couldn't match image
        return HttpResponse(json.dumps({'stat': 'face_unmatched'}))
    
    if is_signed_in is None:
        return HttpResponse(
            "<h1>Please Log in First or Sign out using the same browser <br> If that doesn't work, you might have cleared the cookies</h1>"
        )
    
    elif is_signed_in == 'N':
        return redirect('/')

    return render(req, 'user/sign_out.html')



def register(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        email = req.POST.get('email')
        dept = req.POST.get('dept')
        imgs = req.FILES.getlist('images')
        
        # Email exists in DB
        if RegisteredUser.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({'stat': False}))


        user_instance = RegisteredUser(name=name, email=email, department=dept)
        user_instance.save()

        for img in imgs:
            UserImage(image=img, user=user_instance).save()

        return HttpResponse(json.dumps({'stat': True}))

    return render(req, 'user/register.html')



def auth_login(req):
    if req.method == 'POST':
        handle = req.POST['handle']
        password = req.POST['password']
        user = authenticate(req, username=handle, password=password)
        if user is not None:
            login(req, user)
            return HttpResponse(json.dumps({'is_user': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'is_user': False}), content_type='application/json')
    else:
        return render(req, "login.html")
