from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from .models import *
from PIL import Image
from . import face_recognize
from datetime import datetime
from pytz import timezone
import json



def home(req):
    is_signed_in = req.session.get('is_signed_in', None)
    username = req.session.get('user_name', None)
    email = req.session.get('user_email', None)

    signed_in = False if is_signed_in == 'N' or is_signed_in is None else True

    if username is None or email is None:
        msg = '<br><br><br>' 
    else:
        msg = f"Username: <b>{username}</b> <br>Email: <b>{email}</b> <br> {'Signed In' if signed_in else 'Signed out'}"

    return render(req, 'home.html', {
        'signed_in': signed_in,
        'msg': msg
    })



def sign_out(req):
    is_signed_in = req.session.get('is_signed_in', None)

    if req.method == 'POST' and is_signed_in == 'Y':
        email = req.session.get('user_email', None)

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
                leave_time = Timing.objects.get(name='main').time_out
                if ((datetime.combine(signout_time.today(), leave_time).replace(tzinfo=timezone('Asia/Dhaka')) - signout_time).total_seconds() < 0):
                    user_log.late_leave = True
                else:
                    user_log.late_leave = False


                # Storing user log to DB
                user_log.time_out = signout_time
                user_log.total_hours = delta_time
                user_log.save()
                req.session['is_signed_in'] = 'N'

                return HttpResponse(json.dumps(
                    {
                        'stat': 'is_user'
                    }
                ))


        # Couldn't match image
        return HttpResponse(json.dumps(
            {
                'stat': 'face_unmatched'
            }
        ))
    
    if is_signed_in is None:
        return HttpResponse(
            "<h1>Please Log in First or Sign out using the same browser <br> If that doesn't work, you might have cleared the cookies</h1>"
        )
    
    elif is_signed_in == 'N':
        return redirect('/')

    return render(req, 'sign_out.html')



def sign_in(req):
    if req.method == 'POST':

        email = req.POST.get('email')
        user = RegisteredUser.objects.filter(email=email).first()

        if user is None:
            return HttpResponse(json.dumps(
                {
                    'stat': 'not_user'
                }
            ))

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
                join_in = Timing.objects.get(name='main').time_in
                delta_time = (datetime.combine(now_time.today(), join_in).replace(tzinfo=timezone('Asia/Dhaka')) - now_time).total_seconds()
                user_log = Log(name=user.name, user=user)
                user_log.late_join = True if delta_time < 0 else False
                user_log.save()

                # Save into Session
                req.session['is_signed_in'] = 'Y'
                req.session['user_id'] = user_log.id
                req.session['user_name'] = ref_img.user.name
                req.session['user_email'] = ref_img.user.email

                return HttpResponse(json.dumps(
                    {
                        'stat': 'is_user'
                    }
                ))

        # Couldn't match image
        return HttpResponse(json.dumps(
            {
                'stat': 'face_unmatched'
            }
        ))

    if req.session.get('is_signed_in', None) == 'Y':
        return redirect('/')
    
    else:
        return render(req, 'sign_in.html')



def register(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        email = req.POST.get('email')
        imgs = req.FILES.getlist('images')

        user_instance = RegisteredUser(name=name, email=email)
        user_instance.save()

        for img in imgs:
            UserImage(image=img, user=user_instance).save()

        return HttpResponse(json.dumps(
            {
                'stat': True
            }
        ))

    return render(req, 'register.html')



@login_required(login_url='/admin/')
def dashboard(req):
    user_logs = Log.objects.all().order_by('-id')
    return render(req, 'dashboard.html', {'logs': user_logs})
